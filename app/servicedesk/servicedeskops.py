from flask import Blueprint, request, jsonify, session
from flask_login import login_required
from app.services.itsm_ticket_service import TicketOpsService
from app.tool import SparkApi, base_tool
from app.config import Config
import os
import app.wenxin.route_openapi as wenxin

sdops_bp = Blueprint('sd_ops', __name__)
ticket_ops_service = TicketOpsService()
spark_api_url = os.getenv('SPARKAI_URL')
spark_app_id = os.getenv('SPARKAI_APP_ID')
spark_api_key = os.getenv('SPARKAI_API_KEY')
spark_api_secret = os.getenv('SPARKAI_API_SECRET')
spark_llm_domain = os.getenv('SPARKAI_DOMAIN')
baseTool = base_tool.BaseTool()
is_first = True

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
    user_text = ticket_ops_service.upload_file(file, user_id)
    file_text = ticket_ops_service.download_from_blob_storage(ticket_ops_service.SYSTEM_PROMPT_CONTAINER_NAME)
    global text, is_first
    if is_first:
        text = baseTool.checklen(baseTool.getText("system", file_text))
        is_first = False
    text = baseTool.checklen(baseTool.getText("user", user_text))
    SparkApi.answer = ""
    SparkApi.main(spark_app_id, spark_api_key, spark_api_secret, spark_api_url, spark_llm_domain, text)
    text = baseTool.checklen(baseTool.getText("assistant", SparkApi.answer))
    return jsonify({'reply':  SparkApi.answer}), 200

# 开单文字描述
@sdops_bp.route('/ticketDesc', methods=['POST'])
@login_required
def ticket_desc():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401
    user_text = request.json.get('message')
    if not user_text:
        return jsonify({'error': 'No message provided'}), 400
    file_text = ticket_ops_service.download_from_blob_storage(ticket_ops_service.SYSTEM_PROMPT_CONTAINER_NAME)
    global text,is_first
    if is_first:
        text = baseTool.checklen(baseTool.getText("system", file_text))
        is_first = False
    text = baseTool.checklen(baseTool.getText("user", user_text))
    SparkApi.answer = ""
    SparkApi.main(spark_app_id, spark_api_key, spark_api_secret, spark_api_url, spark_llm_domain, text)
    text = baseTool.checklen(baseTool.getText("assistant", SparkApi.answer))
    return jsonify({'reply': SparkApi.answer}), 200