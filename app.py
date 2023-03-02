from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os

upload_folder = 'uploads'
allowed_extension = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config["upload_folder"] = upload_folder


def allowed_file(file_name):
    return '.' in file_name and \
        file_name.rsplit(".", 1)[1].lower() in allowed_extension


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['upload_folder'], name)
    # return redirect("/")


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        file = request.files['img']
        # if the user does not select a file and upload it
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['upload_folder'], filename))
            # return redirect(url_for('download_file', name=filename))
            return redirect(request.url)
        # if len(os.listdir(app.config['upload_folder'])) >= 1:
    images = os.listdir(app.config['upload_folder'])
    fileurl = app.config['upload_folder']
    return render_template("index.html", images=images, fileurl=fileurl)


# function to delete images
@app.route('/delete/<img>')
def method_name(img):
    os.remove(os.path.join(app.config['upload_folder'], img))
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=10)
