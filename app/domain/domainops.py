# fileops_bp.py

from flask import Blueprint, request, jsonify, session
from flask_login import login_required
from app.services.file_ops_service import FileOpsService

domainops_bp = Blueprint('domain_ops', __name__)
file_ops_service = FileOpsService()

@domainops_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    user_id = session['user_id']
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        uploaded_file = file_ops_service.upload_file(file, user_id)
        return jsonify({
            'message': 'File uploaded successfully',
            'text': uploaded_file.content}), 200
    else:
        return jsonify({'error': 'File must be a PDF'}), 400

@domainops_bp.route('/getFile', methods=['GET'])
@login_required
def getFile():
    filename = request.args.get('filename')
    content = file_ops_service.get_file_content(filename)
    return jsonify({
        'message': 'File content retrieved',
        'text': content}), 200

@domainops_bp.route('/history', methods=['GET'])
@login_required
def get_upload_history():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    user_id = session['user_id']
    file_data = file_ops_service.get_upload_history(user_id)
    return jsonify(file_data), 200

@domainops_bp.route('/deleteFile', methods=['POST'])
@login_required
def delete_file():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    data = request.get_json()
    file_id = data.get('fileId')
    user_id = session['user_id']
    if file_ops_service.delete_file(user_id, file_id):
        return jsonify({'message': '删除成功'}), 200
    else:
        return jsonify({'error': '文件没找到，刷新页面试试'}), 404