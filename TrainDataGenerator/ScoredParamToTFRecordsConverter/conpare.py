import tensorflow as tf

from tqdm import tqdm
from tkinter import Tk
import numpy as np

from ImageEnhancer.util import get_image_enhancer
from ScoredParamIO.scored_param_reader import get_scored_param_list

from TrainDataGenerator.ScoredParamToTFRecordsConverter.util \
    import get_dataset_save_dir, SwitchableTFRecordsWriter

from random import randint
from PIL.Image import Image

class ScoredParamConverter:
    def __init__(self):


def _make_label(left_score: float, right_score: float):
    if left_score > right_score:
        return 0

    if right_score > left_score:
        return 1

    if left_score == right_score:
        return randint(0, 1)

def write(writer: SwitchableTFRecordsWriter,
          left_image: Image, right: Image, label: int):
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

    example = tf.train.Example(features=features)
    record = example.SerializeToString()
    writer.write(record)


if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()

    image_enhancer = get_image_enhancer()
    scored_param_list = get_scored_param_list()
    save_file_dir = get_dataset_save_dir()
    root.destroy()

    train_rate, valid_rate, test_rate = 0.7, 0.2, 0.1

    scored_param_length = len(scored_param_list)

    data_length = sum(range(scored_param_length-1))
    train_data_length = data_length*train_rate
    validation_data_length = data_length*(train_rate+valid_rate)

    writer = \
        SwitchableTFRecordsWriter(
            save_file_dir, train_data_length, validation_data_length)

    for left_index in tqdm(range(0, scored_param_length-1),
                           desc='left data'):
        for right_index in tqdm(range(left_index+1, scored_param_length),
                                desc='right data'):
            left_param = scored_param_list[left_index]
            right_param = scored_param_list[right_index]

            left_image = image_enhancer.resized_enhance(left_param)
            right_image = image_enhancer.resized_enhance(right_param)

            left_array = np.asarray(left_image)
            right_array = np.asarray(right_image)

            left_score = scored_param_list[left_index]['score']
            right_score = scored_param_list[right_index]['score']

            label = _make_label(left_score, right_score)

            write(writer, left_image, right_image, label)
            writer.count_up()

    print('\n')

    print('--- complete ! ---')
