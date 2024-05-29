import os

import psutil
import platform
from flask import Flask, render_template, redirect, send_from_directory


def get_drives():
    try:
        drives = []
        for disk in psutil.disk_partitions():
            drives.append(disk.mountpoint)
        return drives
    except PermissionError:
        return ["/"] if platform.system() == "Linux" else ["Not defined"]


def cd(path):
    os.chdir(path.replace("/", "\\") if platform.system() == "Windows" else path)
    return os.getcwd()


def file_icon(filename):
    file_type = filename.split(".")[-1]
    extensions = {
        "txt": "text-icon",
        "xlsx": "excel-icon",
        "docx": "word-icon",
        "doc": "word-icon",
        "pdf": "pdf-icon",
        "exe": "exe-icon",
        "zip": "archive-icon",
        "7z": "archive-icon",
        "rar": "rar-icon",
        "mp4": "video-icon",
        "mkv": "video-icon",
        "avi": "video-icon",
        "flv": "video-icon",
        "webm": "video-icon",
        "wmv": "video-icon",
        "png": "image-icon",
        "jpg": "image-icon",
        "jpeg": "image-icon",
        "gif": "image-icon",
        "bmp": "image-icon",
        "raw": "image-icon"
    }
    return extensions.get(file_type.lower(), "unknown-icon")


app = Flask(__name__)


@app.route('/')
def main_page():
    try:
        dir_contents = []
        for i in os.scandir(os.getcwd()):
            content_dic = {
                "path": i.path,
                "name": i.name,
                "isDir": i.is_dir(),
                "isFile": i.is_file(),
                "isSymlink": i.is_symlink(),
                "icon": "folder-icon" if i.is_dir() else file_icon(i.name)
            }
            dir_contents.append(content_dic)

        if len(os.getcwd().replace("\\", "/").split("/")) > 1 and os.getcwd().replace("\\", "/").split("/")[1] != '':
            dir_contents.insert(0, True)
        else:
            dir_contents.insert(0, False)

        return render_template("main_page.html", dir_contents=dir_contents, drives=get_drives(), current_drive=os.getcwd().split("/")[0] + "\\" if platform.system() == "Windows" else "/" + os.getcwd().split("/")[1],current_path=os.getcwd())
    except FileNotFoundError:
        return render_template("error.html", error_title="File not found error", error_description="requested file removed or you don't have system permission to see this folder")


@app.route("/download/<path:filepath>")
def download(filepath):
    filename = filepath.split("/")[-1]
    dir = filepath.split(filename)[0]
    try:
        return send_from_directory(dir, filename)
    except PermissionError:
        return render_template("error.html", error_title="Permission denied",
                               error_description="Sorry but you don't have permission to download this file!")


@app.route("/prev_dir")
def prev_dir():
    prev_path = os.getcwd().replace("\\", "/").split("/")
    print(len(prev_path) > 1 and prev_path[1] != '')
    if len(prev_path) > 1 and prev_path[1] != '':
        del prev_path[-1]
        if len(prev_path) > 1:
            cd("/".join(prev_path))
        else:
            cd(prev_path[0] + "/")
        return redirect("/")


@app.route("/chdir/<path:dirpath>")
def change_directory(dirpath):
    try:
        cd(dirpath)
        return redirect("/")
    except PermissionError:
        return render_template("error.html", error_title="Permission denied",
                               error_description="Sorry but you don't have permission to open this folder")


if __name__ == '__main__':
    app.run(debug=True, port=8000)
