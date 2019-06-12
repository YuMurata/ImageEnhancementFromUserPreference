from pathlib import Path
from tkinter.filedialog import askdirectory
import tensorflow as tf

IMAGE_WIDTH, IMAGE_HEIGHT = 32, 32
IMAGE_CHANNEL = 3

TRAIN = 'train'
VALIDATION = 'validation'
TEST = 'test'

DATASET_TYPE_LIST = [TRAIN, VALIDATION, TEST]
EXTENSION = '.tfrecords'

TRAINDATA_PATH = 'C: /Users/init/Documents/PythonScripts/ \
        PredictEvaluationFromHumanPreference/TrainData/'


class SwitchableTFRecordsWriter:
    def __init__(self, save_file_dir: str, train_data_length: int,
                 validation_data_length: int):
        self.writer_dict = \
            {key: tf.python_io.TFRecordWriter(
                str(Path(save_file_dir)/(key+EXTENSION)))
                for key in DATASET_TYPE_LIST}
        self.writer_switcher = 0
        self.count = 0
        self.train_data_length = train_data_length
        self.validation_data_length = validation_data_length

    def count_up(self):
        self.count += 1

        if self.count < self.train_data_length:
            self. writer_switcher = 0
        elif self.count < self.validation_data_length:
            self.writer_switcher = 1
        else:
            self.writer_switcher = 2

    def write(self, record: str):
        self.writer_dict[DATASET_TYPE_LIST[self.writer_switcher]] \
            .write(record)


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
