import random, string
import time

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import session
import logging


# 生成验证码
def generate_captcha():
    def rndColor():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def rndChar():
        return random.choice(string.ascii_letters + string.digits)

    width, height = 120, 50
    image = Image.new('RGB', (width, height), 'white')
    font = ImageFont.truetype('arial.ttf', 40)  # 确保你有这个字体文件，或者指定其他字体
    draw = ImageDraw.Draw(image)

    captcha_text = ''.join(rndChar() for _ in range(4))
    session['captcha'] = captcha_text.lower()  # 存储在session中，用于后续验证

    for t in range(4):
        draw.text((10 + t * 28, 5), captcha_text[t], font=font, fill=rndColor())

    for _ in range(2):
        x1 = random.randint(0, int(width / 2))
        y1 = random.randint(0, int(height / 2))
        x2 = random.randint(0, width)
        y2 = random.randint(int(height / 2), height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    image = image.filter(ImageFilter.GaussianBlur(radius=1.5))
    return image, captcha_text


def recode(fun):
    def f(**pa):
        logging.info(time.ctime())
        fun(**pa)
        logging.info(time.ctime())
    return f

class BaseTool():
    def __init__(self):
        self.__text = []
    def getText(self, role, content):
        jsoncon = {}
        jsoncon["role"] = role
        jsoncon["content"] = content
        self.__text.append(jsoncon)
        return self.__text

    def getlength(self, text):
        length = 0
        for content in text:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length

    def checklen(self, text=None):
        if text == None:
            text = self.__text
        while (self.getlength(text) > 8000):
            if len(text) == 1:
                text[0]['content'] = text[0]['content'][1:8000]
            else:
                del text[0]
        return text

    def text(self):
        return self.__text


