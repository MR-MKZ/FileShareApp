import os
import platform

try:
    import psutil
    from flask import Flask, render_template, redirect, send_from_directory
except ModuleNotFoundError:
    if platform.system() == "Windows":
        os.system("pip install -r requirements.txt")
    else:
        try:
            os.system("sudo pip install -r requirements.txt")
        finally:
            try:
                os.system("sudo pip3 install -r requirements.txt")
            finally:
                print("Is pip installed on your system?")


def get_drives():
    try:
        drives = []
        for disk in psutil.disk_partitions():
            drives.append(disk.mountpoint)
        return drives
    except PermissionError:
        return ["/"] if platform.system() == "Linux" else ["Not defined"]


def cd(path):
    os.chdir(path if platform.system() == "Windows" else "/" + path)
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
        entries = os.scandir(os.getcwd())
        sorted_entries = sorted(entries, key=lambda entry: entry.name)
        for i in sorted_entries:
            preview_types = ["mp4",
                         "mkv",
                         "avi",
                         "flv",
                         "webm",
                         "wmv",
                         "png",
                         "jpg",
                         "jpeg",
                         "gif"]
            file_extension = i.name.split(".")[-1]

            if file_extension in preview_types:
                has_preview = True
            else:
                has_preview = False

            content_dic = {
                "path": i.path,
                "name": i.name,
                "isDir": i.is_dir(),
                "isFile": i.is_file(),
                "isSymlink": i.is_symlink(),
                "icon": "folder-icon" if i.is_dir() else file_icon(i.name),
                "preview": has_preview
            }
            dir_contents.append(content_dic)

        if len(os.getcwd().replace("\\", "/").split("/")) > 1 and os.getcwd().replace("\\", "/").split("/")[1] != '':
            dir_contents.insert(0, True)
        else:
            dir_contents.insert(0, False)

        if platform.system() == "Windows":
            current_drive = os.getcwd().split("\\")[0] + "\\"
        else:
            current_drive = "/" + os.getcwd().split("/")[1]

        return render_template("main_page.html",
                               dir_contents=dir_contents,
                               drives=get_drives(),
                               current_drive=current_drive,
                               current_path=os.getcwd())

    except FileNotFoundError:
        current_file_path = os.path.abspath(__import__('inspect').getsourcefile(lambda: 0)).split("/")
        del current_file_path[-1]
        cd("\\".join(current_file_path)) if platform.system() == "Windows" else cd("/".join(current_file_path))
        return render_template("error.html", error_title="File not found error",
                               error_description="requested file removed or you don't have system permission to see this folder")


@app.route("/download/<path:filepath>")
def download(filepath):
    filename = filepath.split("/")[-1]
    dir = filepath.split(filename)[0]
    try:
        return send_from_directory(dir if platform.system() == "Windows" else "/" + dir, filename)
    except PermissionError:
        return render_template("error.html", error_title="Permission denied",
                               error_description="Sorry but you don't have permission to download this file!")


@app.route("/prev_dir")
def prev_dir():
    prev_path = os.getcwd().replace("\\", "/").split("/")
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
        return render_template("error.html",
                               error_title="Permission denied",
                               error_description="Sorry but you don't have permission to open this folder")


if __name__ == '__main__':
    # HOST = socket.gethostname()
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("8.8.8.8", 80))
    # IP = s.getsockname()[0]
    # print(f'Enter http://{IP}:8000 in your browser')
    try:
        app.run(debug=True, port=8000, host="0.0.0.0")
    except:
        app.run(debug=True, port=8000, host="127.0.0.1")
