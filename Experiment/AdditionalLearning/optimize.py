from PreferenceOptimizer import ParameterOptimizer
from UserPreferencePredictor.Model import RankNet
import config
from IEFUP.ImageEnhancer import ResizableEnhancer
from IEFUP.Optimize import EnhanceGenerator, EnhanceDecorder
from pathlib import Path


if __name__ == "__main__":
    enhance_decoder = EnhanceDecorder()

    cnn = RankNet(config.IMAGE_SHAPE, use_vgg16=False)

    weights_path = r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\AdditionalLearning\weights\16-0.28-0.22.h5'
    cnn.load(weights_path)

    optimize_dir_path = Path(r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\AdditionalLearning\optimize')

    for image_name, path_list in config.image_path_dict.items():
        for index, image_path in enumerate(path_list):
            enhancer = ResizableEnhancer(image_path, config.IMAGE_SIZE)
            enhance_generator = EnhanceGenerator(enhancer)

            cnn_best_param_list, _ = ParameterOptimizer(
                cnn, enhance_generator, enhance_decoder).optimize(ngen=10)

            save_dir_path = optimize_dir_path/image_name/str(index)
            save_dir_path.mkdir(parents=True, exist_ok=True)
            for index, best_param in enumerate(cnn_best_param_list):
                save_path = str(save_dir_path/f'best_{index}.png')
                enhancer.enhance(best_param).save(save_path)
