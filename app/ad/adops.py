# fileops_bp.py

from flask import Blueprint, request, jsonify, session
from flask_login import login_required
from app.services.file_ops_service import FileOpsService

adops_bp = Blueprint('ad_ops', __name__)
file_ops_service = FileOpsService()

@adops_bp.route('/getPic', methods=['POST'])
@login_required
def getPic():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401
    pic_names = []
    contents = file_ops_service.get_pic(pic_names)
    return jsonify({
        'picList': contents}), 200