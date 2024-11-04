from flask import Blueprint, request, send_from_directory, redirect, url_for, render_template_string, jsonify
import os
from PyPDF2 import PdfFileReader
# from docx import Document
from app.config import upload_folder,download_folder
from pdfminer.high_level import extract_text


fileops_bp = Blueprint('file_ops', __name__)


@fileops_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)

        # 提取PDF中的文本
        doc = extract_text(filepath)

            # 你可以在这里添加将文本保存到数据库或返回给客户端的逻辑
        return jsonify({'message': 'File uploaded successfully', 'text': doc}), 200
    else:
        return jsonify({'error': 'File must be a PDF'}), 400


@fileops_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(upload_folder, filename)


@fileops_bp.route('/downloads/<filename>')
def download(filename):
    return send_from_directory(download_folder, filename, as_attachment=True)

