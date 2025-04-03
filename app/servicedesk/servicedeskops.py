from datetime import datetime

from flask import Blueprint, request, jsonify, session
from flask_login import login_required

from app.services.azure_service import AzureService
from app.services.ticket_service import TicketService
from app.tool import base_tool
import app.wenxin.route_openapi as wenxin
import os
from app.config import upload_folder
from werkzeug.utils import secure_filename
import logging

sdops_bp = Blueprint('sd_ops', __name__)
baseTool = base_tool.BaseTool()
text = []
ticket_service = TicketService()

def create_ticket_to_LLM(user_text, index):
    file_text = AzureService.download_from_blob_storage(os.getenv('SYSTEM_PROMPT_CONTAINER_NAME'), os.getenv('SYSTEM_PROMPT_BLOB_NAME')).read().decode('utf-8')
    global text
    text = baseTool.checklen(baseTool.getText("user", user_text))
    user_id = session['user_id']
    AzureService.upload_to_blob_storage(container_name=os.getenv('USER_PROMPT_CONTAINER_NAME'), blob_name=str(user_id) + str(datetime.now()) + '.txt', data=user_text)
    payload = {
        "messages": text,
        "system": file_text
    }
    response = wenxin.send_request_to_baidu_api(payload)
    result = response.get('result')[15:-3]
    if response.get('error_code') is not None:
        return response.get('error_msg')

    text = baseTool.getText("assistant", result)
    ticket_service.add_ticket(index=index, message=user_text, reply=result, user_id=session['user_id'])
    return result

# 针对每个回答点赞点踩
@sdops_bp.route('/goodorbad', methods=['POST'])
@login_required
def good_or_bad():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401
    judge = request.json.get('goodorbad')
    index = request.json.get('index')
    ticket = ticket_service.get_ticket_by_index(index)
    ticket_service.add_ticket(ticket=ticket, good_bad=judge)

#开单问题历史列表
@sdops_bp.route('/tickethistory', methods=['POST'])
@login_required
def ticket_history():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401
    tickets = ticket_service.get_ticket_history(session['user_id'])
    return jsonify({'reply':tickets})

@sdops_bp.route('/submitTicket', methods=['POST'])
@login_required
def submit_ticket():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401
    index = request.json.get('index')


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
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # index = request.form.get('index')
    user_id = session['user_id']
    user_text = AzureService.upload_file(file, user_id)
    return jsonify({'reply': user_text})

# 开单文字描述
@sdops_bp.route('/ticketDesc', methods=['POST'])
@login_required
def ticket_desc():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    user_text = request.json.get('message')
    index = request.json.get('index')
    if not user_text:
        return jsonify({'error': 'No message provided'}), 400

    return jsonify({'reply': create_ticket_to_LLM(user_text, index)})

