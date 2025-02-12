from app.tool import SparkApi, base_tool

spark_api_url = 'wss://spark-api.xf-yun.com/v1.1/chat'
spark_app_id = '2707106d'
spark_api_key = '2414198145407f1db4a56a87253e25aa'
spark_api_secret ='M2M4MzcxNzg4YjhkMjc5YmU0NjZjMGY5'
spark_llm_domain = 'lite'

baseTool = base_tool.BaseTool()
text = ""

while True:
    user_input = input('user:')
    if user_input == "exit":
        break
    text = baseTool.checklen(baseTool.getText("user", user_input))
    SparkApi.answer = ""
    SparkApi.main(spark_app_id, spark_api_key, spark_api_secret, spark_api_url, spark_llm_domain, text)
    text = baseTool.checklen(baseTool.getText("assistant", SparkApi.answer))
