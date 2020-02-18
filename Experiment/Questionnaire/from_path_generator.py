from UserPreferencePredictor.TrainDataMaker.data_generator import DataGenerator
from pathlib import Path
from PIL import Image


class FromPathGeneratorException(Exception):
    pass


class FromPathGenerator(DataGenerator):
    def generate(self, file_path: str):
        file_path = Path(file_path)

        if not file_path.exists():
            raise FromPathGeneratorException(f'{file_path} is not found')

        return Image.open(str(file_path)).convert('RGB')

    def resized_generate(self, param):
        raise FromPathGeneratorException('no use')

    def get_param_num(self):
        raise FromPathGeneratorException('no use')

    def get_param_keys(self):
        raise FromPathGeneratorException('no use')

    def reshape_param(self, param_list: list):
        raise FromPathGeneratorException('no use')
