
from flask import Flask, render_template, request, redirect, send_from_directory, abort
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ADMIN_PASSWORD = 'rohan321'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

batches = {
    '243': {'notes': ['TBA', 'TBA', 'TBA']},
    '251': {'notes': ['Introductory', 'Maths', 'BDS']},
    '252': {'notes': ['Biophysical', 'Biology', 'English']},
}

@app.route('/')
def home():
    return render_template('index.html', batches=batches)

@app.route('/batch/<batch_id>')
def batch_page(batch_id):
    if batch_id not in batches:
        return "Batch Not Found", 404
    return render_template('batch.html', batch_id=batch_id, notes=batches[batch_id]['notes'])

@app.route('/upload/<batch_id>/<section>', methods=['GET', 'POST'])
def upload_file(batch_id, section):
    section_folder = os.path.join(app.config['UPLOAD_FOLDER'], batch_id, section)
    os.makedirs(section_folder, exist_ok=True)
    files = os.listdir(section_folder)

    if request.method == 'POST':
        if 'delete' in request.form:
            password = request.form.get('password')
            if password != ADMIN_PASSWORD:
                return abort(403)
            filename = request.form.get('delete')
            os.remove(os.path.join(section_folder, filename))
            return redirect(request.url)

        password = request.form.get('password')
        if password != ADMIN_PASSWORD:
            return abort(403)
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(section_folder, filename))
            return redirect(request.url)

    return render_template('upload.html', files=files, batch_id=batch_id, section=section)

@app.route('/download/<batch_id>/<section>/<filename>')
def download_file(batch_id, section, filename):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], batch_id, section)
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/tba')
def tba():
    return render_template('tba.html')

@app.route('/members/<batch_id>')
def members(batch_id):
    members_list = [
        {'name': f'Member {i+1}', 'photo': 'https://via.placeholder.com/150'} for i in range(25)
    ]
    return render_template('members.html', batch_id=batch_id, members=members_list)

if __name__ == '__main__':
    app.run(debug=True)
