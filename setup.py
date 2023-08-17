import os
import socket
from argparse import ArgumentParser
from pathlib import Path
from platform import system

from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from FILE_TYPES import FILE_TYPES

app = Flask(__name__)
app.debug = True

port = 5000
dot_files = False
OS_SYSTEM = system()


def get_file_size(file):
    size = os.path.getsize(file)
    size = round(size / 1024)
    return f"{size:.1f} kb"


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


def get_windows_data(path, drive):
    data = dict()
    data["path"] = path
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
    data["localhost"] = socket.gethostbyname(socket.gethostname())
    data["port"] = port
    data["drive"] = drive
    return data


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
    elif OS_SYSTEM == "linux":
        path = f"{os.path.expanduser('~')}{os.sep}{path}{os.sep}"
    return send_from_directory(path, file, as_attachment=True)


@app.route("/upload/", methods=["POST"])
def upload_file():
    try:
        f = request.files["file"]
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
    args = parser.parse_args()
    port = args.port if args.port else 5000
    dot_files = True if args.dot_files and args.dot_files != "0" else False

    app.run(host="0.0.0.0", port=port)
