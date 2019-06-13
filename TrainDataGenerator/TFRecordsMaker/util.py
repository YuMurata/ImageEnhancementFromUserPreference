from pathlib import Path
from tkinter.filedialog import askdirectory

IMAGE_WIDTH, IMAGE_HEIGHT = 32, 32
IMAGE_CHANNEL = 3

TRAIN = 'train'
VALIDATION = 'validation'
TEST = 'test'

DATASET_TYPE_LIST = [TRAIN, VALIDATION, TEST]
EXTENSION = '.tfrecords'

TRAINDATA_PATH = 'C: /Users/init/Documents/PythonScripts/ \
        PredictEvaluationFromHumanPreference/TrainData/'


def get_dataset_dir():
    dataset_dir = \
        askdirectory(
            title='データセットがあるフォルダを選択してください')

    if not dataset_dir:
        raise FileNotFoundError('フォルダが選択されませんでした')

    return dataset_dir


def get_dataset_save_dir():
    dataset_dir = \
        askdirectory(
            title='データセットを保存するフォルダを選択してください')

    if not dataset_dir:
        raise FileNotFoundError('フォルダが選択されませんでした')

    return dataset_dir


def make_dataset_path_dict(dataset_dir: str):
    dataset_path_dict = \
        {key: str(Path(dataset_dir)/(key+EXTENSION))
         for key in DATASET_TYPE_LIST}
    return dataset_path_dict
