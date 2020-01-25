from color_transfer.color_transfer import color_transfer
import cv2
from IEFUP.submodule import ImageRankNet
from IEFUP.ImageRankNet.mycnn import MyCNN
from IEFUP.Optimize \
    import EnhanceGenerator, EnhanceDecorder, Predictor, Optimizer
from pathlib import Path
import pickle
from gdrive_scripts import config

if __name__ == "__main__":
    optimize_dir_path = Path(__file__).parent / 'optimize'
    weights_dir_path = Path(__file__).parent / 'weights'
    optimizable_dir_path = Path(__file__).parent / 'optimizable'
    target_dir_path = Path(__file__).parent / 'target' / 'image'

    for category_dir_path in optimizable_dir_path.iterdir():
        category_name = category_dir_path.name
        weight_path = weights_dir_path / f'{category_name}.h5'

        for image_path in category_dir_path.iterdir():

            generator = EnhanceGenerator(
                str(image_path), config.ImageInfo.size)
            enhance_decoder = EnhanceDecorder()

            predictor = Predictor(config.ImageInfo.shape, str(weight_path))

            optimizer = Optimizer(predictor, generator, enhance_decoder)
            best_param_list, logbook = optimizer.optimize(
                ngen=20, param_list_num=1)

            save_dir_path = optimize_dir_path / category_name
            save_dir_path.mkdir(exist_ok=True)

            enhance_dir_path = save_dir_path / 'enhance'
            enhance_dir_path.mkdir(exist_ok=True)

            image_name = image_path.stem
            enhance_path = str(enhance_dir_path / f'{image_name}.png')
            generator.enhancer.enhance(best_param_list[0]).save(enhance_path)

            transfer_dir_path = save_dir_path / 'transfer'
            transfer_dir_path.mkdir(exist_ok=True)

            optimizable = cv2.imread(str(image_path))
            target = cv2.imread(str(target_dir_path / f'{category_name}.png'))
            cv2.imwrite(
                str(transfer_dir_path / f'{image_name}.png'),
                color_transfer(optimizable, target))
