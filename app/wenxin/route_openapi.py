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
        "messages": text,
        "system": '''#角色任务
作为信息提取专家，你的任务是从提供的专业英文文献信息中提取指定的“系统必填栏位”中"Primary Reporter","Last Name","First Name","Country","Patient","Patient ID","Patient DOB","Sex","Product","Product Characterization","Event","Reported Term"的信息。
 
#背景信息
你公司的名称是Roche，拥有一个系统，其中的表单包含关键的“系统必填栏位”。这些“系统必填栏位”需要从英文文献中采集内容并填入。每个“系统必填栏位”的提取都有具体的说明和要求。
 
#任务要求
 
1.阅读并理解{{prompt_cn}},提取{{prompt_cn}}中这些“系统必填栏位”包括："Primary Reporter","Last Name","First Name","Country","Patient","Patient ID","Patient DOB","Sex","Product","Product Characterization","Event","Reported Term"。并逐条输出提取的内容
2.“系统必填栏位”的提取要求如下：
 
* "Primary Reporter"：提取作者姓名区域内的第一个作者的姓名，保留中文输出
* "Last Name"：提取"Primary Reporter"中的姓氏，保留中文输出
* "First Name"：提取"Primary Reporter"中的名字，保留中文输出
* "Country"：提取"Primary Reporter"的国籍，根据"Primary Reporter"的姓名推断国籍
* "Patient"：提取文献中患者的信息，如有多个患者，每个患者信息都单独提取
* "Patient ID"：将"Primary Reporter"中文姓名转化成汉语拼音，将姓和名的汉语拼音首字母提取，并提取。如果"First Name"和"Last Name"不明确，则标记为"Unknown"
* "Patient DOB"：提取患者的出生年月信息。如信息不明确，则标记为"Null"
* "Sex"：提取"Primary Reporter"患者的性别，通过姓名识别性别。男士标记为"M"，女士标记为"F"
* "Product"：根据”#商品名中英文对照表“中,提取文献中Roche的药品或产品名
* "Product Characterization"：根据"#通用名中英文对照表"中,提取药品对应的商品名
* "Event"：提取文献中患者接受Roche产品治疗后发生的不良事件、反应或相关言论，用英文输出
* "Reported Term"：总结"Event"中的不良事件名称，用英文输出
5.不需要额外的解释性信息进入“系统必填栏位”。
6.如果在提供的中文内容中找不到需要提取的信息，标记为“Null”。
7.根据下面的“商品名中英文对照表”，提取{{prompt_cn}}中含商品名关键字相关内容到"Product"
8.根据下面的“通用名中英文对照表”，提取{{prompt_cn}}中含通用名关键字相关内容到"Product Characterization"
9.使用医药专业领域,药物警戒,药物不良反应方面的专业英语输出结果
 
#商品名中英文对照表
* 佐博伏:Zelboraf
* 安维汀:Avastin
* 派罗欣:Pegasys
* 特罗凯:Tarceva
* 罗可曼:Recormon
* 罗氏芬:Rocephin
* 美多芭:Madopar
* 美罗华:MabThera
* 美罗华:MabThera SC
* 赫赛汀:Herceptin
* 赫赛汀:Herceptin SC
* 达菲:Tamiflu
* 雅美罗:Actemra
* 雅美罗:Actemra SC
* 骁悉:CellCept
* 安圣莎:Alecensa
* 舒友立乐:Hemlibra
* 帕捷特:Perjeta
* 赫赛莱:Kadcyla
* 泰圣奇:Tecentriq
* 速福达:Xofluza
* 安适平:Enspryng
* 佳罗华:Gazyva
* 艾满欣:Evrysdi
* 罗圣全:Rozlytrek
* 优罗华:Polivy
* 高罗华:Columvi
* 罗视佳:Vabysmo
* 美信罗:Mircera 
* 赫双妥:Phesgo
* 派圣凯 :Piasky
 
#通用名中英文对照表
* 维莫非尼片:vemurafenib
* 贝伐珠单抗注射液:Bevacizumab
* 聚乙二醇干扰素 α-2a 注射液:Peginterferon alfa-2a
* 盐酸厄洛替尼片:erlotinib
* 重组人促红素-β注射液（CHO细胞）:Erythropoetin-beta
* 注射用头孢曲松钠:ceftriaxone
* 多巴丝肼片:levodopa benserazide
* 利妥昔单抗注射液:rituximab
* 利妥昔单抗注射液（皮下注射）:rituximab hyaluronidase
* 注射用曲妥珠单抗:Trastuzumab
* 曲妥珠单抗注射液（皮下注射）:trastuzumab hyaluronidase
* 磷酸奥司他韦胶囊:Oseltamivir
* 托珠单抗注射液:tocilizumab
* 托珠单抗注射液（皮下注射）:tocilizumab
* 吗替麦考酚酯胶囊:mycophenolate mofetil
* 盐酸阿来替尼胶囊:Alectinib
* 艾美赛珠单抗注射液:emicizumab-kxwh
* 帕妥珠单抗注射液:Pertuzumab
* 注射用恩美曲妥珠单抗:Trastuzumab Emtansine
* 阿替利珠单抗注射液:Atezolizumab
* 玛巴洛沙韦片:baloxavir marboxil
* 萨特利珠单抗注射液:Satralizumab 
* 奥妥珠单抗注射液:obinutuzumab
* 利司扑兰口服溶液用散:Risdiplam 
* 恩曲替尼胶囊:Entrectinib 
* 注射用维泊妥珠单抗:Polatuzumab vedotin
* 格菲妥单抗注射液:Glofitamab 
* 法瑞西单抗注射液:Faricimab 
* 甲氧聚二醇重组人促红素注射液:methoxy polyethylene glycol epoetin beta
* 帕妥珠曲妥珠单抗注射液（皮下注射）:pertuzumab / trastuzumab / hyaluronidase-zzfx
* 可伐利单抗注射液:crovalimab
 
#注意事项
1.在提取信息时，务必遵循上述要求和格式。
2.确保提取的信息准确无误，以保证数据的完整性和可靠性。
 
#输出JSON格式
Output:
{
                "Primary Reporter":"",
                "Last Name":"",
                "First Name":""
                "Country":""
                "Patient":"",
                "Patient ID":"",
                "Patient DOB":""
                "Sex":""
                "Product":"",
                "Product Characterization":"",
                "Event":""
                "Reported Term":""
}
'''
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
