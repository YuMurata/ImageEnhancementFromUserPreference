from tkinter import Tk
from ImageEnhancer.util import get_image_enhancer
from ScoredParamIO.scored_param_reader import get_scored_param_list
from TrainDataGenerator.TFRecordsMaker.util \
    import get_dataset_save_dir

from TrainDataGenerator.TFRecordsMaker.util import DATASET_TYPE_LIST
from conpare import convert as compare_convert
from regression import convert as regression_convert
from UserPreferencePredictor.Model.util \
    import set_model_type_args, MODEL_TYPE_LIST, ArgumentParser

if __name__ == "__main__":
    args = set_model_type_args(ArgumentParser()).parse_args()

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
        dict(zip(DATASET_TYPE_LIST, [0.7, 0.2, 0.1]))

    convert_func_dict = \
        dict(zip(MODEL_TYPE_LIST, [compare_convert, regression_convert]))

    convert_func_dict[args.model_type](save_file_dir, image_enhancer,
                                       scored_param_list, rate_dict)

    print('--- complete ! ---')
