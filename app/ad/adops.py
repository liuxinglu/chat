# fileops_bp.py
import os

from flask import Blueprint, request, jsonify, session, Response, stream_with_context
from flask_login import login_required
from app.services.azure_service import AzureService

adops_bp = Blueprint('ad_ops', __name__)

@adops_bp.route('/getPic/<blob_name>', methods=['POST'])
@login_required
def getPic(blob_name):
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401
    blob_client = AzureService.get_blob_client(os.getenv('PICTURE_CONTAINER_NAME'), blob_name)

    def generate():
        downloader = blob_client.download_blob()  # 这将返回一个StorageStreamDownloader对象
        for chunk in downloader.chunks():  # 或者使用downloader.chunks()进行分块读取
            yield chunk

    headers = {
        'Content-Type': 'image/jpeg',
        'Content-Disposition': f'inline; filename="{blob_name}"'
    }

    return Response(stream_with_context(generate()), headers=headers)