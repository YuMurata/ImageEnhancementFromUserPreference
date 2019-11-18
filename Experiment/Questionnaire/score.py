from TrainDataGenerator.tournament.comparer import CompareCanvasGroupFrame
from tkinter import Tk, Toplevel
from argparse import ArgumentParser, Namespace
from TrainDataGenerator.tournament.game import TournamentGame
from pathlib import Path
from TrainDataGenerator.data_generator import DataGenerator
import TrainDataGenerator.tournament.DataWriter.scored_image as DW_scored_image
import TrainDataGenerator.tournament.DataWriter.scored_param as DW_scored_param
from PIL import Image
from config.path import root_image_dir_path, root_scored_image_dir_path, root_scored_param_dir_path
from misc import get_save_dir_path, get_save_file_path


class MakeTrainDataException(Exception):
    pass


class ImageGenerator(DataGenerator):
    def generate(self, file_path: str):
        file_path = Path(file_path)

        if not file_path.exists():
            raise MakeTrainDataException(f'{file_path} is not found')

        return Image.open(str(file_path)).convert('RGB')

    def resized_generate(self, param):
        raise MakeTrainDataException('no use')

    def get_param_num(self):
        raise MakeTrainDataException('no use')

    def get_param_keys(self):
        raise MakeTrainDataException('no use')

    def reshape_param(self, param_list: list):
        raise MakeTrainDataException('no use')


def _get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-u', '--user_name', required=True)
    parser.add_argument('-i', '--image_name', required=True)
    parser.add_argument('-n', '--image_number', required=True)

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


def score(root: Tk, user_name: str, image_name: str, image_number: str):
    image_dir_path = root_image_dir_path/image_name/image_number/'random_enhance_10'

    if not image_dir_path.exists():
        raise FileNotFoundError
    elif not image_dir_path.is_dir():
        raise NotADirectoryError

    game = TournamentGame(list(map(str, image_dir_path.iterdir())),
                          ImageGenerator())

    scored_image_dir = get_save_dir_path(
        root_scored_image_dir_path, user_name, f'{image_name}/{image_number}')
    scored_param_dir = get_save_dir_path(
        root_scored_param_dir_path, user_name, f'{image_name}/{image_number}')
    scored_param_path = get_save_file_path(scored_param_dir, 'scored_param.json')

    data_writer_list = [
        DW_scored_image.ScoredImageWriter(str(scored_image_dir)),
        DW_scored_param.ScoredParamWriter(str(scored_param_path))
    ]

    sub_win = Toplevel(root)
    canvas = CompareCanvasGroupFrame(
        sub_win, game, data_writer_list=data_writer_list)
    canvas.pack()

    canvas.disp_enhanced_image()
    canvas.focus_set()

    sub_win.grab_set()
    sub_win.wait_window()


if __name__ == "__main__":
    args = _get_args()
    root = Tk()
    root.withdraw()
    score(root, args.user_name, args.image_name, args.image_number)
