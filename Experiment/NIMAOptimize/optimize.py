from IEFUP.NIMA import NIMA, ModelType
from argparse import ArgumentParser
from pathlib import Path
from IEFUP.ImageEnhancer import ResizableEnhancer
from IEFUP.Optimize import EnhanceDecorder, EnhanceGenerator
from UserPreferencePredictor.PreferenceOptimizer import Optimizer


IMAGE_SIZE = (224, 224)
IMAGE_SHAPE = IMAGE_SIZE+(3,)


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-w', '--weights_file_path', required=True)
    parser.add_argument('-i', '--image_name', required=True)
    parser.add_argument('-n', '--image_number', required=True)
    parser.add_argument('-u', '--user_name', required=True)

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


if __name__ == "__main__":
    # args = _get_args()
    root_optimize_dir_path = Path(
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\NIMAOptimize\optimize')
    ranknet_weights_path = r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\summary\dobashi\20-0.39-0.32_dobashi_flower.h5'

    image_dir_path_dict = {
        'katsudon': Path(r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Image\Photography\katsudon'),
        'farm': Path(r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Image\Photography\farm'),
        'waterfall': Path(r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Image\Photography\waterfall')
    }

    model_dict = {
        model_type.name: NIMA(IMAGE_SHAPE, model_type)
        for model_type in list(ModelType)
    }

    for image_name, image_dir_path in image_dir_path_dict.items():
        for index, image_path in enumerate(image_dir_path.iterdir(), start=1):
            optimize_dir_path = root_optimize_dir_path/image_name/str(index)

            enhancer = ResizableEnhancer(image_path, IMAGE_SIZE)
            image_generator = EnhanceGenerator(enhancer)

            for model_name, model in model_dict.items():
                save_dir_path = optimize_dir_path/model_name
                save_dir_path.mkdir(exist_ok=True, parents=True)
                best_param_list, _ = Optimizer(
                    model, image_generator, EnhanceDecorder()).optimize(40)

                for index, best_param in enumerate(best_param_list):
                    save_path = str(Path(save_dir_path)/f'best_{index}.png')
                    enhancer.enhance(best_param).save(save_path)
