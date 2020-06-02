# coding:utf-8

from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("myFile[]")
        print(len(uploaded_files))
        print(uploaded_files)

        # 当前文件所在路径
        basepath = os.path.dirname(__file__)

        for file in uploaded_files:
            if not file.filename.endswith(".pdf"):
                print("文件格式非PDF")
                return
            upload_path = os.path.join(basepath, 'static/file', secure_filename(file.filename))
            file.save(upload_path)

    return render_template('upload1.html')


if __name__ == '__main__':
    app.run(debug=True)
