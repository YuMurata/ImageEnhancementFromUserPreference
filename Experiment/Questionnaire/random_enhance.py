from argparse import ArgumentParser
from pathlib import Path

from UserPreferencePredictor.TrainDataMaker.image_parameter_generator import generate_image_parameter_list
from IEFUP.ImageEnhancer import ImageEnhancer
from IEFUP.ImageEnhancer import enhance_name_list
from tqdm import tqdm


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-i', '--image_path', required=True)
    parser.add_argument('-o', '--output_dir_path', required=True)
    parser.add_argument('-n', '--generate_num', required=True, type=int)

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


def generate_image(enhancer: ImageEnhancer, save_dir_path: Path, generate_num: int):
    param_list = generate_image_parameter_list(enhance_name_list, generate_num)
    for index, param in enumerate(tqdm(param_list)):
        enhancer.org_enhance(param).save(
            str(save_dir_path/f'{index:0=3}.png'))


if __name__ == "__main__":
    args = _get_args()
    image_path = Path(args.image_path)
    output_dir_path = Path(args.output_dir_path)

    if not image_path.exists():
        raise FileNotFoundError

    enhancer = ImageEnhancer(str(image_path), (100, 100))

    save_dir_path = output_dir_path/f'random_enhance_{args.generate_num}'
    save_dir_path.mkdir(exist_ok=True, parents=True)
    generate_image(enhancer, save_dir_path,
                   args.generate_num)
