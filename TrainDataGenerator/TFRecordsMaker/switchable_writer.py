import tensorflow as tf
from pathlib import Path


class SwitchableWriter:
    TRAIN, VALIDATION, TEST = 'train', 'validation', 'test'
    DATASET_TYPE_LIST = [TRAIN, VALIDATION, TEST]
    EXTENSION = '.tfrecords'

    def __init__(self, save_file_dir: str):
        self.writer_dict = \
            {key: tf.python_io.TFRecordWriter(
                str(Path(save_file_dir)/(key+self.EXTENSION)))
                for key in self.DATASET_TYPE_LIST}
        self.switcher = self.TRAIN

    def write(self, record: str):
        self.writer_dict[self.switcher].write(record)
