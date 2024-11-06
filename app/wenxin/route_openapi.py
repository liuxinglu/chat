import requests
import json
import os
from flask import Blueprint, request, jsonify,session
from app.tool import base_tool

openapi_bp = Blueprint('wenxin_openapi', __name__)
text = []
baseTool = base_tool.BaseTool()
conversation_id = ""
app_id = os.getenv('APP_ID')


def get_access_token():
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={os.getenv('API_KEY')}&client_secret={os.getenv('SECRET_KEY')}"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    return response.json().get("access_token")

@openapi_bp.route('/chat', methods=['POST'])
def chat():
    global text
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-128k?access_token=" + get_access_token()

    text = baseTool.checklen(baseTool.getText("user", user_input))
    payload = {
        "messages": text
    }

    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload, verify=False)
    rep = json.loads(response.text)
    print(response.text)

    text = baseTool.checklen(baseTool.getText("assistant", rep.get('result')))
    return jsonify({'reply': rep.get('result')})

@openapi_bp.route('/getKeyword', methods=['POST'])
def getKeyword():
    global text
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-128k?access_token=" + get_access_token()

    text = baseTool.getText("user", user_input)
    payload = {
        "messages": text
    }

    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload, verify=False)
    rep = json.loads(response.text)
    print(response.text)

    if rep.get('error_code')  is not None:
        return jsonify({'reply': rep.get('error_msg')})
    text = baseTool.getText("assistant", rep.get('result'))
    return jsonify({'reply': rep.get('result')})
