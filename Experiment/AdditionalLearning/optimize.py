from IEFUP.submodule import ParameterOptimizer
from IEFUP.ImageEnhancer import ResizableEnhancer
from IEFUP.Optimize import EnhanceGenerator, EnhanceDecorder, Predictor
from pathlib import Path
from gdrive_scripts import config


if __name__ == "__main__":
    optimizable_dir_path = Path(__file__).parent / 'optimizable'
    weights_dir_path = Path(__file__).parent / 'weights'
    optimize_dir_path = Path(__file__).parent / 'optimize'

    for category_name in ['farm', 'flower', 'katsudon', 'waterfall']:
        weight_file_path = str(weights_dir_path / f'{category_name}.h5')

        for image_file_path in optimizable_dir_path.iterdir():
            image_name = image_file_path.stem
            print(f'optimize {image_name} in {category_name}')

            generator = EnhanceGenerator(
                str(image_file_path), config.ImageInfo.size)
            enhance_decoder = EnhanceDecorder()

            predictor = Predictor(str(weight_file_path))

            optimizer = \
                ParameterOptimizer.Optimizer(predictor, generator,
                                             enhance_decoder)
            best_param_list, logbook = optimizer.optimize(
                ngen=20, param_list_num=1)

            save_dir_path = optimize_dir_path / category_name
            save_dir_path.mkdir(exist_ok=True)

            enhance_path = str(save_dir_path / f'{image_name}.png')
            generator.enhancer.enhance(best_param_list[0]).save(enhance_path)
