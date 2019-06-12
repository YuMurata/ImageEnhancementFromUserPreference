from TrainDataGenerator.TFRecordsMaker.base_maker import BaseMaker

import numpy as np
import tensorflow as tf


class CompareMaker(BaseMaker):
    def __init__(self, save_dir: str):
        super(CompareMaker, self).__init__(save_dir)

    def write(self, left_array: np.array, right_array: np.array, label: int):
        features = \
            tf.train.Features(feature={
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

        self._write(features)
