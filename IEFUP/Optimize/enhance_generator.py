from IEFUP.submodule import ParameterOptimizer
from IEFUP.ImageEnhancer \
    import ResizableEnhancer, enhance_name_list, MIN_PARAM, MAX_PARAM
import numpy as np


class EnhanceGeneratorException(Exception):
    pass


class EnhanceGenerator(ParameterOptimizer.DataGenerator):
    def __init__(self, image_path: str, resized_size: tuple):
        self.enhancer = ResizableEnhancer(image_path, resized_size)

    def generate(self, param):
        return self.enhancer.resized_enhance(param)
