from pprint import pprint
from TrainDataGenerator.TFRecordsMaker.util \
    import make_dataset_path_dict, TRAIN, VALIDATION
from UserPreferencePredictor.Model.util \
    import MODEL_BUILDER_DICT,  COMPARE, TRAINABLE, MODEL_TYPE_LIST
from argparse import ArgumentParser

from datetime import datetime
from pathlib import Path
import tensorflow as tf


def _make_summary_dir(summary_dir_path: str):
    now = datetime.now()
    path = Path(summary_dir_path)/'{0:%m%d}'.format(now)/'{0:%H%M}'.format(now)

    if path.exists():
        path = Path(str(path.parent)+'_{0:%S}'.format(now))

    path.mkdir(parents=True)

    return str(path)


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-d', '--dataset_dir_path', required=True)
    parser.add_argument('-s', '--summary_dir_path', required=True)
    parser.add_argument('-l', '--load_dir_path')
    parser.add_argument('-t', '--model_type', choices=MODEL_TYPE_LIST,
                        required=True)
    parser.add_argument('-j', '--use_jupyter', action='store_true')

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


if __name__ == "__main__":
    args = _get_args()

    model_type = args.model_type

    batch_size = 100 if model_type == COMPARE else 10
    model_builder = MODEL_BUILDER_DICT[model_type][TRAINABLE]
    summary_dir_path = _make_summary_dir(args.summary_dir_path)

    trainable_model = \
        model_builder(batch_size, summary_dir_path, tf.Graph(),
                      is_use_jupyter=args.use_jupyter)

    if args.load_dir_path:
        try:
            trainable_model.restore(args.load_dir_path)
        except ValueError:
            trainable_model.initialize_variable()
    else:
        trainable_model.initialize_variable()

    dataset_path_dict = make_dataset_path_dict(args.dataset_dir_path)

    epoch_num = 10
    train_metrics = \
        trainable_model.fit(dataset_path_dict[TRAIN], epoch_num)

    pprint(train_metrics)
    print('')

    trainable_model.save(summary_dir_path)

    validation_metrics = \
        trainable_model.inference(dataset_path_dict[VALIDATION])
    pprint(validation_metrics)
    print('')

    print('--- complete ! ---')
