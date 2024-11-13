from flask import Blueprint, request, send_from_directory, g, jsonify,session
import os
from app.config import upload_folder,download_folder
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename

fileops_bp = Blueprint('file_ops', __name__)


@fileops_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(upload_folder, secure_filename(file.filename))
        file.save(filepath)

        # 提取PDF中的文本
        doc = extract_text(filepath)
        return jsonify({
            'message': 'File uploaded successfully',
            'text': doc}), 200
    else:
        return jsonify({'error': 'File must be a PDF'}), 400


@fileops_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(upload_folder, filename)


@fileops_bp.route('/downloads/<filename>')
def download(filename):
    return send_from_directory(download_folder, filename, as_attachment=True)

@fileops_bp.route('/getFile', methods=['GET'])
def getFile():
    filename = request.args.get('filename')
    print(filename)
    filepath = os.path.join(upload_folder, filename)
    doc = extract_text(filepath)
    return jsonify({
        'message': 'File uploaded successfully',
        'text': doc}), 200

