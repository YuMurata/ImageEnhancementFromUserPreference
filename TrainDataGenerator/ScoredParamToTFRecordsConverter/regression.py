import tensorflow as tf

from tqdm import tqdm
from tkinter import Tk
import numpy as np

from TrainDataGenerator.ScoredParamToTFRecordsConverter.util \
    import IMAGE_HEIGHT, IMAGE_WIDTH, get_dataset_save_dir, \
    SwitchableTFRecordsWriter

from ImageEnhancer.util import get_image_enhancer
from ScoredParamIO.scored_param_reader import get_scored_param_list


if __name__ == "__main__":
    root = Tk()
    root.attributes('-topmost', True)

    root.withdraw()
    root.lift()
    root.focus_force()

    image_enhancer = get_image_enhancer()
    scored_param_list = get_scored_param_list()
    save_file_dir = get_dataset_save_dir()

    root.destroy()

    train_rate, valid_rate, test_rate = 0.7, 0.2, 0.1

    data_length = len(scored_param_list)

    train_data_length = data_length*train_rate
    validateion_data_length = data_length*(train_rate+valid_rate)

    writer = \
        SwitchableTFRecordsWriter(
            save_file_dir, train_data_length, validateion_data_length)

    max_score = max(scored_param_list, key=lambda x: x['score'])['score']

    for scored_param \
            in tqdm(scored_param_list, desc='write TFRecords'):

        image = image_enhancer.enhance(scored_param) \
            .resize((IMAGE_WIDTH, IMAGE_HEIGHT))

        image_array = np.asarray(image)

        score = scored_param['score']/max_score

        features = \
            tf.train.Features(
                feature={
                    'score':
                    tf.train.Feature(
                        float_list=tf.train.FloatList(value=[score])),
                    'image':
                    tf.train.Feature(
                        bytes_list=tf.train.BytesList(
                            value=[image_array.tobytes()])),
                }
            )

        example = tf.train.Example(features=features)
        record = example.SerializeToString()
        writer.write(record)

        writer.count_up()

    print('\n')

    print('--- complete ! ---')
