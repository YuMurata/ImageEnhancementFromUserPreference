import UserPreferencePredictor.Model.Compare.train as compare_train
from argparse import ArgumentParser

from config.path import root_summary_dir_path
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


def train(user_name: str, image_name: str, tfrecords_dir_path: str):
    try:
        summary_dir_path = get_save_dir_path(
            root_summary_dir_path, user_name, image_name)

        compare_train.train(summary_dir_path, tfrecords_dir_path)
    except (MiscException, compare_train.TrainModelException) as e:
        raise TrainPredictorException(e)


if __name__ == "__main__":
    args = _get_args()

    train(args.user_name, args.image_name, args.tfrecords_dir_path)
