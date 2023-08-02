import os
import socket

from pathlib import Path

from flask import Flask, render_template, send_from_directory

from FILE_TYPES import FILE_TYPES

app = Flask(__name__)
app.debug = True

port = 5000


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
    path = path.replace("-", "/")
    if not path:
        selected_path = f"{os.path.expanduser('~')}/"
    else:
        selected_path = os.path.expanduser("~") + f"/{path}/"

    files = os.listdir(selected_path)
    data["dirs"] = [
        f for f in files if os.path.isdir(selected_path + f) and not f.startswith(".")
    ]
    data["files"] = [
        f for f in files if os.path.isfile(selected_path + f) and not f.startswith(".")
    ]
    data["dirs"].sort()
    data["files"].sort()
    data["files"] = determine_file_types(data["files"], selected_path)
    data["prev_dir"] = (
        str(Path(f"/{path}").parent.absolute()).replace("/", "-")[1:] if path else None
    )
    data["full_path"] = selected_path
    data["append_slash"] = "-" if path else ""
    data["localhost"] = socket.gethostbyname(socket.gethostname())
    data["port"] = port

    return render_template("index.html", **data)


@app.route("/download/<path>/<file>/")
def download_file(path="", file=""):
    path = path.replace("-", "/")
    path = os.path.expanduser("~") + f"/{path}/"
    return send_from_directory(path, file, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
