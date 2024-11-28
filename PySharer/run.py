from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from argparse import ArgumentParser

from .FILE_TYPES import FILE_TYPES

from platform import system

import socket
import math
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(current_dir, "templates"),
    static_folder=os.path.join(current_dir, "static"),
)
app.debug = False

port = 5050
dot_files = False
download = True
upload = True
OS_SYSTEM = system().lower()


def get_file_size(file):
    sizes = ["Bytes", "KB", "MB", "GB", "TB"]
    size = os.path.getsize(file)
    if size == 0:
        return "0 Byte"
    i = int(math.floor(math.log(size) / math.log(1024)))
    return str(round(size / math.pow(1024, i), 2)) + " " + sizes[i]


def get_files(path):
    data = dict()
    data["dirs"] = list()
    data["files"] = list()
    list_dot_files = "" if dot_files else " and not f.startswith('.')"
    files = os.listdir(path)

    for f in files:
        if eval(f"os.path.isdir(path+f){list_dot_files}"):
            data["dirs"].append(f)

    for f in files:
        if eval(f"os.path.isfile(path+f){list_dot_files}"):
            data["files"].append(f)

    data["dirs"].sort()
    data["files"].sort()
    return data


def determine_file_types(files, path):
    data = list()
    for file in files:
        size = get_file_size(path + file)
        data.append(
            dict(
                name=file,
                type=FILE_TYPES.get(file[file.rfind(".") + 1 :].lower(), "unknown"),
                size=size,
            )
        )
    return data


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    try:
        # use network to detect perfect IPV4 address
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        # sometimes return localhost instead of IPV4 address
        ip = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return ip


def get_windows_data(path, drive):
    data = dict()
    data["download"] = download
    data["upload"] = upload
    data["path"] = path
    if download:
        if path or drive:
            path = path.replace("~", os.sep)
            selected_path = f"{drive}:{os.sep}{path}{os.sep}"

            data.update(get_files(selected_path))
            data["files"] = determine_file_types(data["files"], selected_path)
            data["full_path"] = selected_path
        else:
            drives = os.popen("wmic logicaldisk get name").read()
            drives = re.findall(r"([^\s]*:)", drives)
            data["drives"] = list(map(lambda x: x[:-1], drives))

    data["prev_dir"] = True if path or drive else False
    data["append_slash"] = "~" if path else ""
    data["localhost"] = get_ip_address()
    data["port"] = port
    data["drive"] = drive
    return data


def get_linux_data(path, drive):
    data = dict()
    data["download"] = download
    data["upload"] = upload
    data["path"] = path
    if download:
        path = path.replace("~", "/")
        if not path:
            selected_path = f"{os.path.expanduser('~')}{os.sep}"
        else:
            selected_path = f"{os.path.expanduser('~')}{os.sep}{path}{os.sep}"

        data.update(get_files(selected_path))
        data["files"] = determine_file_types(data["files"], selected_path)
        data["full_path"] = selected_path

    data["prev_dir"] = True if path else False
    data["append_slash"] = "~" if path else ""
    data["localhost"] = get_ip_address()
    data["port"] = port

    return data


def get_darwin_data(path, drive):
    return get_linux_data(path, drive)


@app.route("/")
@app.route("/<path>/")
def main(path=""):
    drive = request.args.get("drive", "")
    data = eval(f"get_{OS_SYSTEM}_data")(path, drive)
    return render_template("index.html", **data)


@app.route("/download/<file>/")
@app.route("/download/<path>/<file>/")
def download_file(path="", file=""):
    drive = request.args.get("drive", "")
    path = path.replace("~", os.sep)
    if OS_SYSTEM == "windows":
        path = f"{drive}:{os.sep}{path}{os.sep}"
    elif OS_SYSTEM == "linux" or OS_SYSTEM == 'darwin':
        path = f"{os.path.expanduser('~')}{os.sep}{path}{os.sep}"
    return send_from_directory(path, file, as_attachment=True)


@app.route("/upload/", methods=["POST"])
def upload_file():
    try:
        files = request.files.getlist("file")
        # f = request.files["file"]
        for f in files:
            file_name = secure_filename(f.filename)
            path = f"{os.path.expanduser('~')}{os.sep}Downloads{os.sep}"
            f.save(path + file_name)
        return jsonify(dict(message="success", code=True)), 201
    except Exception as e:
        return (
            jsonify(
                dict(
                    message="There comes an error while uploading your file.<br>Please try another file!",
                    code=False,
                )
            ),
            500,
        )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--port")
    parser.add_argument("--dot_files")
    parser.add_argument("--download")
    parser.add_argument("--upload")
    args = parser.parse_args()
    port = args.port if args.port else port
    dot_files = True if args.dot_files and args.dot_files != "0" else False
    download = False if args.download and args.download == "0" else True
    upload = False if args.upload and args.upload == "0" else True

    app.run(host="0.0.0.0", port=port)
