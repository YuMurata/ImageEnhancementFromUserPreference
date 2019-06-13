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

        self.dataset_iter = iter(self.DATASET_TYPE_LIST)
        self.switcher = self.dataset_iter.__next__()

    def write(self, record: str):
        self.writer_dict[self.switcher].write(record)


class AutoSwitchableWriter(SwitchableWriter):
    def __init__(self, save_file_dir: str, rate_dict: dict, data_length: int):
        super(AutoSwitchableWriter, self).__init__(save_file_dir)

        self.write_count_dict = {key: 0 for key in self.DATASET_TYPE_LIST}
        self.data_length_dict = \
            {key: int(data_length * rate_dict[key])
                for key in self.DATASET_TYPE_LIST}

    def write(self, record: str):
        super(AutoSwitchableWriter, self).write(record)

        self.write_count_dict[self.switcher] += 1

        write_count = self.write_count_dict[self.switcher]
        data_length = self.data_length_dict[self.switcher]

        if write_count > data_length:
            try:
                self.switcher = self.dataset_iter.__next__()
            except StopIteration:
                self.switcher = self.TRAIN
