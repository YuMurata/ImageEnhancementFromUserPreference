from PreferenceOptimizer import ParameterOptimizer
from UserPreferencePredictor.Model import RankNet
import config
from IEFUP.ImageEnhancer import ResizableEnhancer
from IEFUP.Optimize import EnhanceGenerator, EnhanceDecorder
from pathlib import Path


if __name__ == "__main__":
    image_path = r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\katsudon\2\2.png'

    enhancer = ResizableEnhancer(image_path, config.IMAGE_SIZE)
    enhance_generator = EnhanceGenerator(enhancer)
    enhance_decoder = EnhanceDecorder()

    cnn = RankNet(config.IMAGE_SHAPE, use_vgg16=False)
    vgg = RankNet(config.IMAGE_SHAPE, use_vgg16=True)

    records_num_list = [50, 100, 150]
    weights_dir_path = Path(
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\VGG16_Change_DataNum\weights')

    optimize_dir_path = Path(
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\VGG16_Change_DataNum\optimize\unknown')

    for records_num in records_num_list:
        cnn_weights_path = str(weights_dir_path/'cnn'/f'{records_num}.h5')
        vgg_weights_path = str(weights_dir_path/'vgg'/f'{records_num}.h5')

        cnn.trainable_model.load_weights(cnn_weights_path)
        vgg.trainable_model.load_weights(vgg_weights_path)

        cnn_best_param_list, _ = ParameterOptimizer(
            cnn, enhance_generator, enhance_decoder).optimize(ngen=10)
        vgg_best_param_list, _ = ParameterOptimizer(
            vgg, enhance_generator, enhance_decoder).optimize(ngen=10)

        def save_optimize(save_dir_path: str, best_param_list: list):
            save_dir_path.mkdir(parents=True, exist_ok=True)
            for index, best_param in enumerate(best_param_list):
                save_path = str(save_dir_path/f'best_{index}.png')
                enhancer.enhance(best_param).save(save_path)

        cnn_optimize_dir_path = optimize_dir_path/'cnn'/str(records_num)
        save_optimize(cnn_optimize_dir_path, cnn_best_param_list)

        vgg_optimize_dir_path = optimize_dir_path/'vgg'/str(records_num)
        save_optimize(vgg_optimize_dir_path, vgg_best_param_list)
