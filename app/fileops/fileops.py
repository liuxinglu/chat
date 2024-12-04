from flask import Blueprint, request, send_from_directory, g, jsonify,session
import os
from app.config import upload_folder,download_folder
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename
from app.model.models import UploadedFile, db
from flask_login import login_required

fileops_bp = Blueprint('file_ops', __name__)


@fileops_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    user_id = session['user_id']
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
        # 将文件信息保存到数据库
        uploaded_file = UploadedFile(filename=file.filename, content=doc, user_id=user_id)
        db.session.add(uploaded_file)
        db.session.commit()
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
@login_required
def getFile():
    filename = request.args.get('filename')
    print(filename)
    filepath = os.path.join(upload_folder, filename)
    doc = extract_text(filepath)
    return jsonify({
        'message': 'File uploaded successfully',
        'text': doc}), 200


@fileops_bp.route('/history', methods=['GET'])
@login_required
def get_upload_history():
    if 'user_id' not in session:
        print('User not authenticated')
        return jsonify({'error': 'User not authenticated'}), 401

    user_id = session['user_id']
    files = UploadedFile.query.filter_by(user_id=user_id).all()
    file_data = [{'fileid': f.id, 'filename': f.filename, 'upload_date': f.upload_date, 'content': f.content} for f in files]
    return jsonify(file_data), 200


@fileops_bp.route('/deleteFile', methods=['POST'])
@login_required
def delete_file():
    if 'user_id' not in session:
        print('User not authenticated')
        return jsonify({'error': 'User not authenticated'}), 401
    data = request.get_json()
    file_id = data.get('fileId')

    user_id = session['user_id']
    file_to_delete = UploadedFile.query.filter_by(user_id=user_id, id=file_id).first()

    if not file_to_delete:
        return jsonify({'error': 'File not found'}), 404

    db.session.delete(file_to_delete)
    db.session.commit()
    return jsonify({'message': '删除成功'}), 200
