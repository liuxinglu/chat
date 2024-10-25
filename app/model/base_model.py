from abc import ABC, abstractmethod
import os


class LargeModel(ABC):
    @abstractmethod
    def load_model(self, model_path: str):
        pass

    @abstractmethod
    def initialize(self, **kwargs):
        pass

    @abstractmethod
    def predict(self, input_data):
        pass

        # 可以添加一个配置方法，用于设置模型的其他配置参数

    @abstractmethod
    def configure(self, **config):
        pass