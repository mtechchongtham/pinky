from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = b'secret'

BASE_PATH = os.path.abspath(os.environ.get('HOME'))
ALLOWED_EXTENSION = {'txt', 'pdf', 'csv', 'xlsx', 'doc'}

def allowed_files(filename) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files.get('file')

        if file.filename == "":
            flash('No file selected')
            return redirect(request.url)

        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(BASE_PATH, '/', filename))
            flash('File Uploaded Successully')
            return redirect(url_for('download'))

        if not allowed_files(file.filename):
            flash('file not supported')
            return redirect(request.url)

    return render_template('index.html')


@app.route('/download', methods=['GET'])
def download():
    return 'Download Page'

if __name__ == '__main__':
    app.run(debug=True)
