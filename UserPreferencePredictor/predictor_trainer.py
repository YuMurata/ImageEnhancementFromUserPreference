import tkinter as tk

from pprint import pprint

from TrainDataGenerator.TFRecordsMaker.util \
    import make_dataset_path_dict, TRAIN, VALIDATION

from UserPreferencePredictor.Model.util \
    import make_summary_dir, get_load_dir, \
    MODEL_BUILDER_DICT, set_model_type_args, COMPARE, TRAINABLE, ArgumentParser

from JupyterUtil.args import set_use_jupyter_args

from TrainDataGenerator.TFRecordsMaker.util \
    import get_dataset_dir

if __name__ == "__main__":
    parser = ArgumentParser()
    parser = set_model_type_args(parser)
    parser = set_use_jupyter_args(parser)
    args = parser.parse_args()

    root = tk.Tk()
    root.attributes('-topmost', True)

    root.withdraw()
    root.lift()
    root.focus_force()

    model_type = args.model_type

    try:
        summary_dir = make_summary_dir()
    except FileNotFoundError:
        print('summary用フォルダが選択されなかったため終了します')
        exit()

    batch_size = 100 if model_type == COMPARE else 10
    model_builder = MODEL_BUILDER_DICT[model_type][TRAINABLE]
    trainable_model = \
        model_builder(batch_size, summary_dir, is_use_jupyter=args.jupyter)

    try:
        load_dir = get_load_dir(model_type)
        trainable_model.restore(load_dir)
    except (FileNotFoundError, ValueError):
        trainable_model.initialize_variable()

    dataset_dir = get_dataset_dir()

    root.destroy()

    dataset_path_dict = make_dataset_path_dict(dataset_dir)

    epoch_num = 10
    train_metrics = \
        trainable_model.fit(dataset_path_dict[TRAIN], epoch_num)

    pprint(train_metrics)
    print('')

    trainable_model.save(summary_dir)

    validation_metrics = \
        trainable_model.inference(dataset_path_dict[VALIDATION])
    pprint(validation_metrics)
    print('')

    print('--- complete ! ---')
