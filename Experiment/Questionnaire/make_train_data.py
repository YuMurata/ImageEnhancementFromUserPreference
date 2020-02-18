from UserPreferencePredictor.TrainDataMaker import Tournament, DataWriter
import tkinter as tk
from argparse import ArgumentParser, Namespace
import config
from misc import get_save_file_path, MiscException, get_save_dir_path
import IEFUP.GDrive as gdrive
from IEFUP.TrainDataMaker.Tournament import EnhancedPlayer
from IEFUP.TrainDataMaker import generate_random_param_list
import random
from IEFUP.ImageEnhancer import ImageEnhancer
import itertools
from IEFUP.TrainDataMaker.Tournament import CompareCanvasGroupFrame


class MakeTrainDataException(Exception):
    pass


def _get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-u', '--user_name', required=True)
    parser.add_argument('-i', '--image_name', required=True)

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


class TrainDataMakerException(MakeTrainDataException):
    pass


def compare(window: tk.Toplevel, image_path: str, scored_param_path: str, compare_num: int) -> bool:
    enhancer = ImageEnhancer(image_path)

    random.seed(0)
    player_list = [EnhancedPlayer(param, enhancer)
                   for param in generate_random_param_list(compare_num)]
    game = Tournament(player_list)

    data_writer_list = [
        DataWriter.ScoredParamWriter(scored_param_path)]

    canvas = CompareCanvasGroupFrame(
        window, game, data_writer_list=data_writer_list)
    canvas.pack()

    canvas.update_image()
    canvas.focus_set()

    window.grab_set()
    window.wait_window()

    return game.is_complete


def make_train_data(root: tk.Tk, user_name: str, image_name: str) -> (bool, str):
    image_dir_path = config.path.root_image_dir_path / \
        image_name/'1'

    if not image_dir_path.exists():
        raise MakeTrainDataException(f'{str(image_dir_path)} is not found')
    elif not image_dir_path.is_dir():
        raise MakeTrainDataException(f'{str(image_dir_path)} is not directory')

    image_path = list(itertools.chain(image_dir_path.glob(
        '*.jpg'), image_dir_path.glob('*.png')))[0]

    try:
        scored_param_dir_path = get_save_dir_path(
            config.path.root_scored_param_dir_path, user_name, image_name)
        scored_param_path = get_save_file_path(
            scored_param_dir_path, 'scored_param'+DataWriter.ScoredParamWriter.SUFFIX)
    except MiscException as e:
        raise MakeTrainDataException(e)

    sub_win = tk.Toplevel(root)
    try:
        compare_num = 100
        is_complete = compare(sub_win, image_path, scored_param_path, compare_num)
        return is_complete, scored_param_path

    except TrainDataMakerException as e:
        sub_win.destroy()
        raise MakeTrainDataException(e)


if __name__ == "__main__":
    args = _get_args()
    root = tk.Tk()
    root.withdraw()
    is_complete, scored_param_path = make_train_data(
        root, args.user_name, args.image_name)

    if is_complete:
        dest_dir_path = f'{gdrive.root_dir}/scored_param/{args.user_name}'
        gdrive.upload(scored_param_path, dest_dir_path, upload_file_name=args.image_name +
                      DataWriter.ScoredParamWriter.SUFFIX)
