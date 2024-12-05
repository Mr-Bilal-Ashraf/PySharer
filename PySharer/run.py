import subprocess
from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from argparse import ArgumentParser

from FILE_TYPES import FILE_TYPES
from version import __version__

from platform import system
from pathlib import Path

import socket
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


def get_file_size(file: Path):
    """
    This function is used to get the size of the file in human readable format.

    :param file: It is the path to the file that is being accessed.
    :return: It is returning the size of the file in human readable format.
    """

    sizes = ["Bytes", "KB", "MB", "GB", "TB"]
    size = file.stat().st_size
    for unit in sizes:
        if size < 1024:
            return str(round(size, 2)) + " " + unit
        size /= 1024


def get_files(path: Path):
    """
    This function is used to get files & directories from the specified path.

    :param path: It is the path to the directory that is being accessed.
    :return: It is returning the data that is being accessed.
    """

    data = dict(
        dirs=list(),
        files=list(),
    )
    list_dot_files = "" if dot_files else " and not f.name.startswith('.')"
    for f in path.iterdir():
        if eval(f"f.is_dir(){list_dot_files}"):
            data["dirs"].append(f.name)

        if eval(f"f.is_file(){list_dot_files}"):
            data["files"].append(f)

    return data


def determine_file_types(files: list):
    """
    This function is used to determine the file type of the files in the specified path.

    :param files: It is the list of files that is being accessed.
    :return: It is returning the data that is being accessed.
    """

    data = list()
    for file in files:
        size = get_file_size(file)
        ext = file.suffix[1:].lower()
        data.append(
            dict(
                name=file.name,
                type=FILE_TYPES.get(ext, "unknown"),
                size=size,
            )
        )
    return data


def get_ip_address():
    """
    This function is used to detect the IPV4 address of the machine. On macOS, it first connects to socket to
    get the IPV4 address, as macOS sometimes returns localhost instead of IPV4 address.
    This IPV4 address is used to show on the homepage.
    :return: IP address of the machine
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

def get_ssid():
    try:
        if OS_SYSTEM == "windows":
            result = subprocess.check_output(
                "netsh wlan show interfaces", shell=True, text=True
            )
            match = re.search(r"SSID\s*:\s*(.+)", result)
            return match.group(1) if match else "Unknown SSID"
        elif OS_SYSTEM == "linux":
            result = subprocess.check_output(
                "nmcli -t -f active,ssid dev wifi", shell=True, text=True
            )
            for line in result.strip().split("\n"):
                if line.startswith("yes:"):
                    return line.split(":")[1]
            return "Unknown SSID"
        elif OS_SYSTEM == "darwin":
            result = subprocess.check_output(
                "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I",
                shell=True,
                text=True,
            )
            match = re.search(r"SSID: (.+)", result)
            return match.group(1) if match else "Unknown SSID"
    except Exception as e:
        return "Unknown SSID"



def get_windows_data(path: str, drive: str):
    """
    This function is used to get files & directories from the specified path on Windows.

    :param path: It is the path to the directory that is being accessed.
    :param drive: It is the drive that is being accessed.
    :return: It is returning the data that is being accessed.
    """

    data = dict()
    data["download"] = download
    data["upload"] = upload
    data["path"] = path
    data["ssid"] = get_ssid()
    if download:
        if path or drive:
            path = path.replace("~", os.sep)
            selected_path = Path(f"{drive}:/") / path

            data.update(get_files(selected_path))
            data["files"] = determine_file_types(data["files"])
            data["full_path"] = selected_path
            data["dirs"].sort(key=str.lower)
            data["files"] = sorted(data["files"], key=lambda x: x["name"].lower())
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


def get_linux_data(path: str, drive: str):
    """
    This function is used to get files & directories from the specified path on linux.

    :param path: It is the path to the directory that is being accessed.
    :param drive: This parameter is not in use in this function because linux have no drives.
    :return: It is returning the data that is being accessed.
    """

    data = dict()
    data["download"] = download
    data["upload"] = upload
    data["path"] = path
    data["ssid"] = get_ssid()
    if download:
        path = path.replace("~", "/")
        selected_path = Path().home()
        if path:
            selected_path = selected_path / path

        data.update(get_files(selected_path))
        data["files"] = determine_file_types(data["files"])
        data["full_path"] = selected_path
        data["files"] = sorted(data["files"], key=lambda x: x["name"].lower())
        data["dirs"].sort(key=str.lower)

    data["prev_dir"] = True if path else False
    data["append_slash"] = "~" if path else ""
    data["localhost"] = get_ip_address()
    data["port"] = port

    return data


def get_darwin_data(path: str, drive: str):
    """
    This function is used to get files & directories from the specified path on macOS.

    :param path: It is the path to the directory that is being accessed.
    :param drive: It is the drive that is being accessed.
    :return: It is returning the data that is being accessed.
    """

    return get_linux_data(path, drive)


@app.route("/")
@app.route("/<path>/")
def main(path: str = ""):
    """
    This is the main API of the app. It is used to get the files & directories from the specified path to showcase
    them using the template. So user can explore and download the required file.

    :param path: It is the path to the directory that is being accessed.
    :return: It is returning the index.html template with the data that is being accessed.
    """

    drive = request.args.get("drive", "")
    data = eval(f"get_{OS_SYSTEM}_data")(path, drive)
    return render_template("index.html", **data)


@app.route("/download/<file>/")
@app.route("/download/<path>/<file>/")
def download_file(path: str = "", file: str = ""):
    """
    This API is used to download files from the system who is running this app.

    :param path: It is the path to the file that is being downloaded.
    :param file: It is the name of the file that is being downloaded.
    :return: It is returning the file that is being downloaded.
    """

    drive = request.args.get("drive", "")
    path = path.replace("~", os.sep)
    if OS_SYSTEM == "windows":
        path = f"{drive}:{os.sep}{path}{os.sep}"
    elif OS_SYSTEM == "linux" or OS_SYSTEM == "darwin":
        path = f"{os.path.expanduser('~')}{os.sep}{path}{os.sep}"
    return send_from_directory(path, file, as_attachment=True)


@app.route("/upload/", methods=["POST"])
def upload_file():
    """
    This API is used to upload files to the Downloads folder of the system who is running this app.
    It can accept multiple files at once.

    It is returning a JSON response with the following keys:
    - message: A string message indicating the status of the upload operation.
    - code: A boolean value indicating whether the upload was successful or not.
    - Note: At the moment, we are not handling these JSON responses in the frontend.
    """

    if not upload:
        return (
            jsonify(
                dict(
                    message="Uploading is disabled by the server admin!",
                    code=False,
                )
            ),
            405,
        )
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


def start():
    """
    Start the PySharer server with the specified arguments from the terminal.
    """

    global app
    global port, dot_files, download, upload
    parser = ArgumentParser(
        description="PySharer is a Flask-based web application for sharing files using LAN."
    )
    parser.add_argument(
        "--version", action="version", version=f"PySharer {__version__}"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5050,
        help="Port number to run the server on (default: 5050)",
    )
    parser.add_argument(
        "--dot_files",
        type=int,
        choices=[0, 1],
        default=0,
        help="Specify whether to show hidden files/directories or not for download. Use 1 for True and 0 for False (default: 0)",
    )
    parser.add_argument(
        "--download",
        type=int,
        choices=[0, 1],
        default=1,
        help="Enable or Disable file download. Use 1 for True and 0 for False (default: 1)",
    )
    parser.add_argument(
        "--upload",
        type=int,
        choices=[0, 1],
        default=1,
        help="Enable or Disable file upload. Use 1 for True and 0 for False (default: 1)",
    )
    args = parser.parse_args()
    port = args.port
    dot_files = bool(args.dot_files)
    download = bool(args.download)
    upload = bool(args.upload)

    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    start()
