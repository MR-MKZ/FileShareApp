from flask import Flask, render_template, redirect, send_from_directory
import win32api
import os


def get_drives():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return drives


def cd(path):
    os.chdir(path)
    return os.getcwd()


app = Flask(__name__)


@app.route('/')
def main_page():
    dir_contents = []
    for i in os.scandir(os.getcwd()):
        content_dic = {
            "path": i.path,
            "name": i.name,
            "isDir": i.is_dir(),
            "isFile": i.is_file(),
            "isSymlink": i.is_symlink()
        }
        dir_contents.append(content_dic)

    if len(os.getcwd().split("\\")) > 1 and os.getcwd().split("\\")[1] != '':
        dir_contents.insert(0, True)
    else:
        dir_contents.insert(0, False)

    return render_template("main_page.html", dir_contents=dir_contents, drives=get_drives(), current_drive=os.getcwd().split("\\")[0] + "\\", current_path=os.getcwd())


@app.route("/download/<path:filepath>")
def download(filepath):
    filename = filepath.split("/")[-1]
    dir = filepath.split(filename)[0]
    try:
        return send_from_directory(dir, filename)
    except PermissionError:
        return redirect("/")

@app.route("/prev_dir")
def prev_dir():
    print(len(os.getcwd().split("\\")) > 1 and os.getcwd().split("\\")[1] != '')
    if len(os.getcwd().split("\\")) > 1 and os.getcwd().split("\\")[1] != '':
        prev_path = os.getcwd().split("\\")
        del prev_path[-1]
        if len(prev_path) > 1:
            cd("\\".join(prev_path))
        else:
            cd(prev_path[0] + "\\")
        return redirect("/")

@app.route("/chdir/<path:dirpath>")
def change_directory(dirpath):
    cd(dirpath)
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, port=8000)
