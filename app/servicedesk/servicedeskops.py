from flask import Blueprint, request, jsonify, session
from flask_login import login_required
from app.services.azure_service import AzureService
from app.tool import base_tool
import app.wenxin.route_openapi as wenxin
import os

sdops_bp = Blueprint('sd_ops', __name__)
baseTool = base_tool.BaseTool()
text = []

def create_ticket_to_LLM(user_text):
    file_text = AzureService.download_from_blob_storage(os.getenv('SYSTEM_PROMPT_CONTAINER_NAME'), os.getenv('USER_PROMPT_BLOB_NAME'))
    global text
    text = baseTool.checklen(baseTool.getText("user", user_text))
    # AzureService.upload_to_blob_storage(os.getenv('USER_PROMPT_CONTAINER_NAME'), os.getenv('USER_PROMPT_BLOB_NAME'), user_text)
    payload = {
        "messages": text,
        "system": file_text
    }
    response = wenxin.send_request_to_baidu_api(payload)
    print(response.get('result'))
    result = response.get('result')[15:-3]
    if response.get('error_code') is not None:
        return response.get('error_msg')

    text = baseTool.getText("assistant", result)
    return result

@sdops_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    user_id = session['user_id']
    user_text = AzureService.upload_file(file, user_id)
    return jsonify({'reply': create_ticket_to_LLM(user_text)})

# 开单文字描述
@sdops_bp.route('/ticketDesc', methods=['POST'])
@login_required
def ticket_desc():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    user_text = request.json.get('message')
    if not user_text:
        return jsonify({'error': 'No message provided'}), 400

    return jsonify({'reply': create_ticket_to_LLM(user_text)})

