import requests
import json
import os
from flask import Blueprint, request, jsonify,session
from app.tool import base_tool
from app.config import Config

openapi_bp = Blueprint('wenxin_openapi', __name__)
text = []
baseTool = base_tool.BaseTool()
conversation_id = ""
app_id = Config.APP_ID


def get_access_token():
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={Config.API_KEY}&client_secret={Config.SECRET_KEY}"
    response = requests.post(url, verify=False)
    response_data = response.json()
    return response_data.get("access_token")

def send_request_to_baidu_api(url, payload):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload, verify=False)
    response_data = response.json()
    return response_data

@openapi_bp.route('/chat', methods=['POST'])
def chat():
    global text
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-128k?access_token=" + get_access_token()
    text = baseTool.checklen(baseTool.getText("user", user_input))
    payload = {"messages": text}
    response = send_request_to_baidu_api(url, payload)
    print(response.get('result'))
    text = baseTool.checklen(baseTool.getText("assistant", response.get('result')))
    return jsonify({'reply': response.get('result')})

@openapi_bp.route('/getKeyword', methods=['POST'])
def getKeyword():
    global text
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-128k?access_token=" + get_access_token()
    text = baseTool.getText("user", user_input)
    current_file_path = os.path.abspath(__file__)
    # 获取当前文件的目录
    current_directory = os.path.dirname(current_file_path)
    with open(os.path.join(os.path.dirname(current_directory), 'static/promt/prompt1.txt'), 'r', encoding='utf-8') as file:
        prompt = file.read()
    payload = {
        "messages": text,
        "system": prompt
    }
    response = send_request_to_baidu_api(url, payload)
    if response.get('error_code')  is not None:
        return jsonify({'reply': response.get('error_msg')})

    print(response.get('result'))
    text = baseTool.getText("assistant", response.get('result'))
    return jsonify({'reply': response.get('result')})

