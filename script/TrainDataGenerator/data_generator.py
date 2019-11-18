from abc import ABCMeta, abstractclassmethod


class DataGenerator(metaclass=ABCMeta):
    @abstractclassmethod
    def generate(self, param):
        pass

    @abstractclassmethod
    def resized_generate(self, param):
        pass

    @abstractclassmethod
    def get_param_num(self):
        pass

    @abstractclassmethod
    def get_param_keys(self):
        pass

    @abstractclassmethod
    def reshape_param(self, param_list: list):
        pass