from tkinter import Tk
from ImageEnhancer.util import get_image_enhancer
from ScoredParamIO.scored_param_reader import get_scored_param_list
from TrainDataGenerator.ScoredParamToTFRecordsConverter.util \
    import get_dataset_save_dir
from argparse import ArgumentParser

from TrainDataGenerator.TFRecordsMaker.switchable_writer \
    import SwitchableWriter
from TrainDataGenerator.ScoredParamToTFRecordsConverter.conpare \
    import convert as compare_convert
from TrainDataGenerator.ScoredParamToTFRecordsConverter.regression \
    import convert as regression_convert

COMPARE = 'compare'
REGRESSION = 'regression'


def _get_args():
    parser = ArgumentParser()
    parser.add_argument('model_type', choices=[COMPARE, REGRESSION])

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

    rate_dict = \
        dict(zip(SwitchableWriter.DATASET_TYPE_LIST, [0.7, 0.2, 0.1]))

    convert_func_dict = \
        dict(zip([COMPARE, REGRESSION], [compare_convert, regression_convert]))

    convert_func_dict[args.model_type](save_file_dir, image_enhancer,
                                       scored_param_list, rate_dict)

    print('--- complete ! ---')
