import os
import appbuilder as ab
from appbuilder.core.console.appbuilder_client import data_class
from flask import Blueprint, request, jsonify, render_template

chat_bp = Blueprint('wenxin', __name__)

client = ab.AppBuilderClient(app_id=os.getenv('APP_ID'))
conversation_id = ""

def ask(user_input):
    global conversation_id
    conversation_id = conversation_id if conversation_id != "" else client.create_conversation()
    message = client.run(conversation_id, user_input)

    response_content = ""
    # 每次迭代返回AppBuilderClientAnswer结构，内可能包括多个事件内容
    for content in message.content:
        # stream=True时，将answer拼接起来才是完整的的对话结果
        response_content += content.answer
        for event in content.events:
            content_type = event.content_type
            detail = event.detail
            # 根据content类型对事件详情进行解析
            if content_type == "code":
                code_detail = data_class.CodeDetail(**detail)
                print(code_detail.code)
            elif content_type == "text":
                text_detail = data_class.TextDetail(**detail)
                print(text_detail.text)
            elif content_type == "image":
                image_detail = data_class.ImageDetail(**detail)
                print(image_detail.url)
            elif content_type == "rag":
                rag_detail = data_class.RAGDetail(**detail)
                if len(rag_detail.references) > 0:
                    print(rag_detail.references)
            elif content_type == "function_call":
                function_call_detail = data_class.FunctionCallDetail(**detail)
                print(function_call_detail.video)
            elif content_type == "audio":
                audio_detail = data_class.AudioDetail(**detail)
                print(audio_detail)
            elif content_type == "video":
                video_detail = data_class.VideoDetail(**detail)
                print(video_detail)
            elif content_type == "status":
                status_detail = data_class.StatusDetail(**detail)
                print(status_detail)
            else:
                default_detail = data_class.DefaultDetail(**detail)
                print(default_detail)

    # 打印完整的answer结果
    print(response_content)

    return response_content


@chat_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # 调用文心一言 API
    reply = ask(user_input)
    print(reply)
    return jsonify({'reply': reply})

