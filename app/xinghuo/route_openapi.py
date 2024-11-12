import os
from flask import Blueprint, request, jsonify
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from app.tool import SparkApi, base_tool

xinghuoapi_bp = Blueprint('xinghuo_api', __name__)

spark_api_url = os.getenv('SPARKAI_URL')
spark_app_id = os.getenv('SPARKAI_APP_ID')
spark_api_key = os.getenv('SPARKAI_API_KEY')
spark_api_secret = os.getenv('SPARKAI_API_SECRET')
spark_llm_domain = os.getenv('SPARKAI_DOMAIN')
baseTool = base_tool.BaseTool()


@xinghuoapi_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    text = baseTool.checklen(baseTool.getText("user", user_input))
    SparkApi.answer = ""
    SparkApi.main(spark_app_id, spark_api_key, spark_api_secret, spark_api_url, spark_llm_domain, text)
    text = baseTool.checklen(baseTool.getText("assistant", SparkApi.answer))
    return jsonify({'reply':  SparkApi.answer.replace('。', '。\n')})

@xinghuoapi_bp.route('/getKeyword', methods=['POST'])
def getKeyword():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    SparkApi.answer = ""
    question = baseTool.checklen(baseTool.getText("user", user_input))
    SparkApi.main(spark_app_id, spark_api_key, spark_api_secret, spark_api_url, spark_llm_domain, question)
    baseTool.getText("assistant", SparkApi.answer)
    return jsonify({'reply':  SparkApi.answer.replace('。', '。\n')})

