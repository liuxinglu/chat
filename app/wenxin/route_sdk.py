import os

from flask import Blueprint, request, jsonify, render_template
import appbuilder

chat_bp = Blueprint('wenxin', __name__)

# 定义prompt模板
template_str = "请回答我的问题。\n\n问题：{question}。\n\n回答："

# 初始化 Playground
playground = appbuilder.Playground(prompt_template=template_str, model="ERNIE Speed-AppBuilder", secret_key=os.getenv('APPBUILDER_TOKEN'))


def ask(user_input):
    # 定义输入
    input_message = appbuilder.Message({"role": 'user', "question": user_input})

    # 调用大模型并流式展示回答内容
    output = playground(input_message, stream=True, temperature=1e-10)
    response_content = ''.join([msg for msg in output.content])

    # 返回完整的对话结果
    result = {
        'response': response_content,
        'details': output.model_dump_json(indent=4)
    }

    return jsonify(result)


@chat_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # 调用文心一言 API
    reply = ask(user_input)
    print(reply.details)
    return jsonify({'reply': reply.response})

