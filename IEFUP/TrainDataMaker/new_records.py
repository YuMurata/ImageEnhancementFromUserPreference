import tensorflow as tf
import numpy as np
from tqdm import tqdm

from UserPreferencePredictor.TrainDataMaker.Tournament.DataWriter import DataWriter, DataWriterException
from UserPreferencePredictor.TrainDataMaker.Tournament import Evaluator

from threading import Thread
from pathlib import Path

from .generate_param import generate_random_param
from IEFUP.ImageEnhancer import ResizableEnhancer

SUFFIX = '.tfrecords'


class TFRecordsWriterException(DataWriterException):
    pass


class Writer:
    def __init__(self, save_file_path: str):
        self.writer = tf.io.TFRecordWriter(save_file_path)

    def write(self, left_array: np.array, right_array: np.array, label: int):
        features = \
            tf.train.Features(
                feature={
                    'label':
                    tf.train.Feature(
                        int64_list=tf.train.Int64List(value=[label])),
                    'left_image':
                    tf.train.Feature(bytes_list=tf.train.BytesList(
                        value=[left_array.tobytes()])),
                    'right_image':
                    tf.train.Feature(bytes_list=tf.train.BytesList(
                        value=[right_array.tobytes()]))
                }
            )

        example = tf.train.Example(features=features)
        record = example.SerializeToString()
        self.writer.write(record)


class WriteThread(Thread):
    def __init__(self, enhancer: ResizableEnhancer, evaluator: Evaluator, generate_num: int, save_file_path: str):
        super(WriteThread, self).__init__()
        self.evaluator = evaluator
        self.save_file_path = save_file_path
        self.generate_num = generate_num
        self.enhancer = enhancer

    def run(self):
        writer = Writer(self.save_file_path)
        for _ in tqdm(range(self.generate_num), desc='write tfrecords'):
            left_param = generate_random_param()
            right_param = generate_random_param()

            left_array = np.array(self.enhancer.resized_enhance(left_param))
            right_array = np.array(self.enhancer.resized_enhance(right_param))

            left_score = self.evaluator.evaluate(left_param)
            right_score = self.evaluator.evaluate(right_param)

            label = 0 if left_score > right_score else 1

            writer.write(left_array, right_array, label)


class TFRecordsWriter(DataWriter):
    def __init__(self, save_file_path: str):
        if Path(save_file_path).suffix != SUFFIX:
            raise TFRecordsWriterException(f'suffix is not {SUFFIX}')

        self.save_file_path = save_file_path

    def write(self, enhancer: ResizableEnhancer, evaluator: Evaluator, generate_num: int):
        write_thread = WriteThread(
            enhancer, evaluator, generate_num, self.save_file_path)
        write_thread.start()
