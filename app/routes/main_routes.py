from flask import Blueprint, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from app.utils.file_ops import allowed_file, save_file

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Dosya bulunamadı', 400
    file = request.files['file']
    if file.filename == '':
        return 'Dosya seçilmedi', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = save_file(file, filename)
        return redirect(url_for('main_bp.result', filename=filename))
    return 'Geçersiz dosya', 400

@main_bp.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)
