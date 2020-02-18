from pathlib import Path
from IEFUP.submodule import ImageRankNet
from IEFUP.ImageRankNet.mycnn import MyCNN
from PIL import Image
import numpy as np

if __name__ == "__main__":
    gradcam_dir_path = Path(__file__).parent / 'gradcam'
    input_dir_path = Path(__file__).parent / 'optimizable'
    weights_dir_path = Path(__file__).parent / 'weights'

    ranknet = ImageRankNet.RankNet(MyCNN())

    for category_name in ['farm', 'flower', 'katsudon', 'waterfall']:
        weight_file_path = str(weights_dir_path / f'{category_name}.h5')

        ranknet.load(weight_file_path)

        for image_path in input_dir_path.iterdir():
            image_name = image_path.stem

            print(f'gradcam {image_name} in {category_name}')

            image_array = np.array(Image.open(str(image_path)).convert('RGB'))
            cam = ranknet.grad_cam.get_cam(image_array, 'conv2d_1')

            save_dir = gradcam_dir_path / category_name
            save_dir.mkdir(exist_ok=True, parents=True)

            Image.fromarray(cam).save(str(save_dir / f'{image_name}.png'))
