from tqdm import tqdm
import numpy as np

from ImageEnhancer.image_enhancer import ImageEnhancer
from ScoredParamIO.scored_param_reader import read_scored_param

from TrainDataGenerator.TFRecordsMaker.compare_maker import CompareMaker
import tensorflow as tf
from argparse import ArgumentParser
from pathlib import Path


def _make_label(left_score: float, right_score: float):
    if left_score > right_score:
        return 0

    elif right_score > left_score:
        return 1

    else:
        raise ValueError('score is same')


def convert(save_file_path: str, image_enhancer: ImageEnhancer,
            scored_param_list: list):
    scored_param_length = len(scored_param_list)

    data_length = 0

    for left_index in range(0, scored_param_length-1):
        for right_index in range(left_index+1, scored_param_length):
            left_param = scored_param_list[left_index]
            right_param = scored_param_list[right_index]

            left_score = scored_param_list[left_index]['score']
            right_score = scored_param_list[right_index]['score']

            if left_score != right_score:
                data_length += 1

    writer = tf.io.TFRecordWriter(save_file_path)
    compare_maker = CompareMaker(writer)

    progress = tqdm(total=data_length)
    for left_index in range(0, scored_param_length-1):
        for right_index in range(left_index+1, scored_param_length):
            left_param = scored_param_list[left_index]
            right_param = scored_param_list[right_index]

            left_image = image_enhancer.resized_enhance(left_param)
            right_image = image_enhancer.resized_enhance(right_param)

            left_array = np.asarray(left_image)
            right_array = np.asarray(right_image)

            left_score = left_param['score']
            right_score = right_param['score']

            try:
                label = _make_label(left_score, right_score)
                compare_maker.write(left_array, right_array, label)
                progress.update()
            except ValueError:
                pass


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-o', '--save_dir_path', required=True)
    parser.add_argument('-i', '--image_path', required=True)
    parser.add_argument('-t', '--train_param_path', required=True)
    parser.add_argument('-v', '--validation_param_path', required=True)

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


def main(image_path: str, train_param_path: str, validation_param_path: str,
         save_dir_path: str):
    image_enhancer = ImageEnhancer(image_path)

    dataset_type_list = ['train', 'validation']

    param_list_dict = {key: read_scored_param(param_file_path)
                       for key, param_file_path
                       in zip(dataset_type_list, (train_param_path,
                                                  validation_param_path))}

    save_dir_path = Path(save_dir_path)
    save_dir_path.mkdir(parents=True, exist_ok=True)

    extension = '.tfrecords'
    records_path_dict = {key: str(save_dir_path/(key+extension))
                         for key in dataset_type_list}

    for key in dataset_type_list:
        convert(records_path_dict[key], image_enhancer, param_list_dict[key])

    print('\n')

    print('--- complete ! ---')


if __name__ == "__main__":
    args = _get_args()
    main(**args)
