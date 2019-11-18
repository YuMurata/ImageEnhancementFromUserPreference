from TrainDataGenerator.tournament.comparer import CompareCanvasGroupFrame
from tkinter import Tk, Toplevel
from argparse import ArgumentParser, Namespace
from TrainDataGenerator.tournament.game import TournamentGame
from pathlib import Path
from TrainDataGenerator.data_generator import DataGenerator
import TrainDataGenerator.tournament.DataWriter.tfrecords as DW_tfrecords
from PIL import Image
from config.path import root_tfrecords_dir_path, root_image_dir_path, root_scored_param_dir_path
from config.dataset import DATASET_TYPE_LIST, TRAIN, VALID
from misc import get_save_dir_path, MiscException, get_save_file_path


class MakeTrainDataException(Exception):
    pass


class ImageGeneratorException(MakeTrainDataException):
    pass


class ImageGenerator(DataGenerator):
    def generate(self, file_path: str):
        file_path = Path(file_path)

        if not file_path.exists():
            raise ImageGeneratorException(f'{file_path} is not found')

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

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


class TrainDataMakerException(MakeTrainDataException):
    pass


class TrainDataMaker:
    def __init__(self, tfrecords_dir_path: str, scored_param_path: str):
        self.tfrecords_dir_path = tfrecords_dir_path
        self.scored_param_path = Path(scored_param_path)

    def compare(self, window: Toplevel, image_dir_path: str, dataset_type: str):
        image_dir_path = Path(image_dir_path)

        if not image_dir_path.exists():
            raise TrainDataMakerException(
                f'{str(image_dir_path)} is not found')
        elif not image_dir_path.is_dir():
            raise TrainDataMakerException(
                f'{str(image_dir_path)} is not directory')

        try:
            game = TournamentGame(list(map(str, image_dir_path.iterdir())),
                                  ImageGenerator())
        except ImageGeneratorException as e:
            raise TrainDataMakerException(e)

        data_writer_list = [
            DW_tfrecords.TFRecordsWriter(get_save_file_path(
                self.tfrecords_dir_path, f'{dataset_type}{DW_tfrecords.SUFFIX}')),
        ]

        canvas = CompareCanvasGroupFrame(
            window, game, data_writer_list=data_writer_list)
        canvas.pack()

        canvas.disp_enhanced_image()
        canvas.focus_set()

        window.grab_set()
        window.wait_window()


def make_train_data(root: Tk, user_name: str, image_name: str):
    image_dir_path = root_image_dir_path/image_name/'1'

    if not image_dir_path.exists():
        raise MakeTrainDataException(f'{str(image_dir_path)} is not found')
    elif not image_dir_path.is_dir():
        raise MakeTrainDataException(f'{str(image_dir_path)} is not directory')

    try:
        tfrecords_dir_path = get_save_dir_path(
            root_tfrecords_dir_path, user_name, image_name)
        scored_param_path = get_save_dir_path(
            root_scored_param_dir_path, user_name, image_name)
    except MiscException as e:
        raise MakeTrainDataException(e)

    maker = \
        TrainDataMaker(tfrecords_dir_path, scored_param_path)

    image_dir_path_dict = {
        key: image_dir_path/f'random_enhance_{n}' for key, n in zip([TRAIN, VALID], [100, 10])}

    for dataset_type in DATASET_TYPE_LIST:
        sub_win = Toplevel(root)
        try:
            maker.compare(sub_win, str(
                image_dir_path_dict[dataset_type]), dataset_type)

        except TrainDataMakerException as e:
            sub_win.destroy()
            raise MakeTrainDataException(e)



if __name__ == "__main__":
    args = _get_args()
    root = Tk()
    root.withdraw()
    make_train_data(root, args.user_name, args.image_name)
