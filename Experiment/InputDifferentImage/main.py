from IEFUP.submodule import ImageRankNet
from IEFUP.ImageRankNet.mycnn import MyCNN
from IEFUP.Optimize \
    import EnhanceGenerator, EnhanceDecorder, Predictor, ParameterOptimizer
from pathlib import Path
from gdrive_scripts import config

if __name__ == "__main__":
    optimize_dir_path = Path(__file__).parent / 'optimize'
    weights_dir_path = Path(__file__).parent / 'weights'
    optimizable_dir_path = Path(__file__).parent / 'optimizable'

    for category_name in ['flower']:
        weight_path = weights_dir_path / f'{category_name}.h5'

        for image_path in optimizable_dir_path.iterdir():
            print(f'optimize {image_path.name} used {category_name}.h5')

            generator = EnhanceGenerator(
                str(image_path), config.ImageInfo.size)
            enhance_decoder = EnhanceDecorder()

            predictor = Predictor(str(weight_path))

            optimizer = \
                ParameterOptimizer.Optimizer(predictor, generator,
                                             enhance_decoder)
            best_param_list, logbook = optimizer.optimize(
                ngen=20, param_list_num=1)

            save_dir_path = optimize_dir_path / category_name
            save_dir_path.mkdir(exist_ok=True, parents=True)

            image_name = image_path.stem
            save_path = str(save_dir_path / f'{image_name}.png')
            generator.enhancer.enhance(best_param_list[0]).save(save_path)
