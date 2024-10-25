from flask import render_template
from app import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


# import os
# import requests
# import json
#
#
# def main():
#     url = "https://qianfan.baidubce.com/v2/app/conversation"
#
#     payload = json.dumps({
#         "app_id": "24d3b987-51d4-4173-aa78-61bb1722e0e2"
#     })
#     headers = {
#         'Content-Type': 'application/json',
#         'X-Appbuilder-Authorization': 'Bearer bce-v3/ALTAK-nI9oFkUMyUmRrpRyM7cZl/7d8883fe9269234e5d6f336bcd5970d27cc47da6'
#     }
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#
#     print(response.text)
#
#
# if __name__ == '__main__':
#     main()
