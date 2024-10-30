import requests
import json
import os
from flask import Blueprint, request, jsonify
from app.tool import base_tool

openapi_bp = Blueprint('wenxin_openapi', __name__)
text = []
baseTool = base_tool.BaseTool()
conversation_id = ""
app_id = os.getenv('APP_ID')


def get_converstation_id():
    url = "https://qianfan.baidubce.com/v2/app/conversation"
    payload = {"app_id": app_id}
    headers = {
        'Content-Type': 'application/json',
        'X-Appbuilder-Authorization': 'Bearer ' + os.getenv('APPBUILDER_TOKEN')
    }
    response = requests.request("POST", url, headers=headers, json=payload, verify=False)

    return json.loads(response.text)['conversation_id']


@openapi_bp.route('/chat', methods=['POST'])
def chat():
    global conversation_id, text
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    url = "https://qianfan.baidubce.com/v2/app/conversation/runs"

    text = baseTool.checklen(baseTool.getText("user", user_input))
    conversation_id = conversation_id if conversation_id != "" else get_converstation_id()
    payload = {
        "app_id": app_id,
        "stream": False,
        "conversation_id": conversation_id,
        "query": user_input,
        "messages": text
    }

    headers = {
        'Content-Type': 'application/json',
        'X-Appbuilder-Authorization': 'Bearer ' + os.getenv('APPBUILDER_TOKEN')
    }
    response = requests.request("POST", url, headers=headers, json=payload, verify=False)
    rep = json.loads(response.text)
    print(response.text)

    conversation_id = rep.get('conversation_id')
    text = baseTool.checklen(baseTool.getText("assistant", rep.get('answer')))
    return jsonify({'reply': rep.get('answer')})
