from abc import ABC, abstractmethod
import os


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

    def checklen(self, text):
        while (self.getlength(text) > 8000):
            if len(text) == 1:
                text[0]['content'] = text[0]['content'][1:8000]
            else:
                del text[0]
        return text