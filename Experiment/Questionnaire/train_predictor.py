import UserPreferencePredictor as upp
from argparse import ArgumentParser

from config.path import root_summary_dir_path
from config.dataset import IMAGE_SHAPE
from misc import get_save_dir_path, MiscException


class TrainPredictorException(Exception):
    pass


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-u', '--user_name', required=True)
    parser.add_argument('-i', '--image_name', required=True)
    parser.add_argument('-t', '--tfrecords_dir_path', required=True)

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


def train(user_name: str, image_name: str, tfrecords_dir_path: str, *, epochs: int = None):
    try:
        def get_summary_dir_path_func():
            return get_save_dir_path(
                root_summary_dir_path, user_name, image_name)

        upp.Model.train_model(
            get_summary_dir_path_func, tfrecords_dir_path, IMAGE_SHAPE, epochs=epochs)
    except (MiscException, upp.Model.TrainModelException) as e:
        raise TrainPredictorException(e)


if __name__ == "__main__":
    args = _get_args()

    train(args.user_name, args.image_name, args.tfrecords_dir_path)
