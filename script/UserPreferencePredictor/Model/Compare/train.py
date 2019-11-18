from TrainDataGenerator.TFRecordsMaker.util \
    import make_dataset_path_dict, TRAIN, VALIDATION
from UserPreferencePredictor.Model.Compare.ranknet import RankNet
from UserPreferencePredictor.Model.Compare.dataset import make_dataset, DatasetException
from .exception import ModelException
from argparse import ArgumentParser

from datetime import datetime
from pathlib import Path


class TrainModelException(ModelException):
    pass


def _make_summary_dir(summary_dir_path: str):
    now = datetime.now()
    path = Path(summary_dir_path)/'{0:%m%d}'.format(now)/'{0:%H%M}'.format(now)

    if path.exists():
        path = Path(str(path.parent)+'_{0:%S}'.format(now))

    path.mkdir(parents=True)

    return str(path)


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-d', '--dataset_dir_path', required=True)
    parser.add_argument('-s', '--summary_dir_path', required=True)
    parser.add_argument('-l', '--load_dir_path')
    parser.add_argument('-j', '--use_jupyter', action='store_true')

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


def train(summary_dir_path: str, dataset_dir_path: str, *, load_dir_path=None):
    batch_size = 100

    trainable_model = RankNet()

    if load_dir_path:
        try:
            trainable_model.load(load_dir_path)
        except ValueError as e:
            raise TrainModelException(e)

    dataset_path_dict = make_dataset_path_dict(dataset_dir_path)

    try:
        dataset = {key: make_dataset(dataset_path_dict[key], batch_size, key)
                   for key in [TRAIN, VALIDATION]}
    except DatasetException as e:
        raise TrainModelException(e)

    trainable_model.train(dataset[TRAIN], log_dir_path=summary_dir_path,
                          valid_dataset=dataset[VALIDATION], epochs=20, steps_per_epoch=30)

    trainable_model.save(summary_dir_path)


if __name__ == "__main__":
    args = _get_args()
    train(**args)
