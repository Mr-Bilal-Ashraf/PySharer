import os
import socket
from argparse import ArgumentParser
from pathlib import Path
from platform import system

from flask import Flask, redirect, render_template, request, send_from_directory
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


@app.route("/")
@app.route("/<path>/")
def main(path=""):
    data = dict()
    data["path"] = path
    path = path.replace("~", "/")
    if not path:
        selected_path = f"{os.path.expanduser('~')}/"
    else:
        selected_path = os.path.expanduser("~") + f"/{path}/"

    files = os.listdir(selected_path)

    list_dot_files = "" if dot_files else " and not f.startswith('.')"
    find_dir = (
        f"[f for f in files if os.path.isdir('{selected_path}' + f){list_dot_files}]"
    )
    find_files = (
        f"[f for f in files if os.path.isfile('{selected_path}' + f){list_dot_files}]"
    )

    data["dirs"] = eval(find_dir)
    data["files"] = eval(find_files)
    data["dirs"].sort()
    data["files"].sort()
    data["files"] = determine_file_types(data["files"], selected_path)
    data["prev_dir"] = (
        str(Path(f"/{path}").parent.absolute()).replace("/", "~")[1:] if path else None
    )
    data["full_path"] = selected_path
    data["append_slash"] = "~" if path else ""
    data["localhost"] = socket.gethostbyname(socket.gethostname())
    data["port"] = port

    return render_template("index.html", **data)


@app.route("/download/<path>/<file>/")
def download_file(path="", file=""):
    path = path.replace("~", "/")
    path = os.path.expanduser("~") + f"/{path}/"
    return send_from_directory(path, file, as_attachment=True)


@app.route("/upload/", methods=["POST"])
def upload_file():
    f = request.files["file"]
    file_name = secure_filename(f.filename)
    path = os.path.expanduser("~") + "/Downloads/"
    f.save(path + file_name)
    return redirect("/", code=302)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--port")
    parser.add_argument("--dot_files")
    args = parser.parse_args()
    port = args.port if args.port else 5000
    dot_files = True if args.dot_files and args.dot_files != "0" else False

    app.run(host="0.0.0.0", port=port)
