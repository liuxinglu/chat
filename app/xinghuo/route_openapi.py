import requests
import json
import os
from flask import Blueprint, request, jsonify, render_template

openapi_bp = Blueprint('wenxin_openapi', __name__)


def get_access_token():

    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={os.getenv('APP_ID')}&client_secret={os.getenv('APPBUILDER_SECRET_KEY')}"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    print(url)
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


@openapi_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ai_apaas_lite?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [{
            "role": "user",
            "content": user_input
        }]
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.headers)
    print(response.text)

    return jsonify(jsonify({'reply': response.text}))


@openapi_bp.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    chat()