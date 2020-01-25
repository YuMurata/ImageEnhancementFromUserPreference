from pathlib import Path
from IEFUP.submodule import ImageRankNet
from IEFUP.ImageRankNet.mycnn import MyCNN
from PIL import Image
import numpy as np

if __name__ == "__main__":
    gradcam_dir_path = Path(__file__).parent / 'gradcam'
    input_dir_path = Path(__file__).parent / 'input'
    weight_dir_path = Path(__file__).parent / 'weight'

    ranknet = ImageRankNet.RankNet(MyCNN())

    for category_dir in input_dir_path.iterdir():
        category_name = category_dir.name
        weight_path = str(weight_dir_path / f'{category_name}.h5')

        ranknet.load(weight_path)

        for image_path in category_dir.iterdir():
            image_array = np.array(Image.open(str(image_path)))
            cam = ranknet.grad_cam.get_cam(image_array, 'conv2d_1')


            save_dir = gradcam_dir_path / category_name
            save_dir.mkdir(exist_ok=True)
            image_name = image_path.stem
            Image.fromarray(cam).save(str(save_dir/ f'{image_name}.png'))
