from abc import ABC, abstractmethod
import os


class BaseTool():
    def __init__(self):
        self.text = []
    def getText(self, role, content):
        jsoncon = {}
        jsoncon["role"] = role
        jsoncon["content"] = content
        self.text.append(jsoncon)
        return self.text

    def getlength(self):
        length = 0
        for content in self.text:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length

    def checklen(self):
        while (self.getlength() > 8000):
            del self.text[0]
        return self.text