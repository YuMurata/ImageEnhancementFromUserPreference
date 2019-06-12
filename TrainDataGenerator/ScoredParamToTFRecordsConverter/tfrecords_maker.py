from tkinter import Tk
from ImageEnhancer.util import get_image_enhancer
from ScoredParamIO.scored_param_reader import get_scored_param_list
from TrainDataGenerator.ScoredParamToTFRecordsConverter.util \
    import get_dataset_save_dir, SwitchableTFRecordsWriter
from argparse import ArgumentParser


def _get_args():
    parser = ArgumentParser()
    parser.add_argument('model_type')

    return parser.parse_args()


if __name__ == "__main__":


    args = _get_args()

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
