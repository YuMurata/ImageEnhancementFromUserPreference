from pathlib import Path


def _init_model_folder(model_folder_path: Path):
    if not model_folder_path.exists():
        model_folder_path.mkdir()

    summary_path = model_folder_path/'summary'
    if not summary_path.exists():
        summary_path.mkdir()

    tfrecords_path = model_folder_path/'tfrecords'
    if not tfrecords_path.exists():
        tfrecords_path.mkdir()


def _init_folder(folder_path: Path):
    compare_folder_path = folder_path/'Compare'
    _init_model_folder(compare_folder_path)

    regression_folder_path = folder_path/'Regression'
    _init_model_folder(regression_folder_path)

    scored_param_folder_path = folder_path/'scored_parameter'
    if not scored_param_folder_path.exists():
        scored_param_folder_path.mkdir()


def make_folder(dl_path: str, dl_num: int):
    folder_index_list = [i+1 for i in range(dl_num)]

    for folder_index in folder_index_list:
        folder_path = Path(dl_path)/str(folder_index)
        if not folder_path.exists():
            folder_path.mkdir()

        _init_folder(folder_path)
