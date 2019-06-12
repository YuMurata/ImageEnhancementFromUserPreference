from tkinter import filedialog, messagebox
from datetime import datetime
from pathlib import Path
from TrainDataGenerator.ScoredParamToTFRecordsConverter.util \
    import TRAINDATA_PATH

from UserPreferencePredictor.Model.Compare.trainable_model \
    import TrainableModel as compare_trainable
from UserPreferencePredictor.Model.Compare.predictable_model \
    import PredictableModel as compare_predictable

from UserPreferencePredictor.Model.Regression.trainable_model \
    import TrainableModel as regression_trainable
from UserPreferencePredictor.Model.Regression.predictable_model \
    import PredictableModel as regression_predictable

from enum import Enum, auto


def make_summary_dir():
    save_dir = \
        filedialog.askdirectory(
            title='学習結果を保存するフォルダを選択してください', initialdir=TRAINDATA_PATH)

    if not save_dir:
        raise FileNotFoundError('フォルダが選択されませんでした')

    now = datetime.now()
    path = Path(save_dir)/'{0:%m%d}'.format(now)/'{0:%H%M}'.format(now)

    if path.exists():
        path = Path(str(path.parent)+'_{0:%S}'.format(now))

    path.mkdir(parents=True)

    return str(path)


def get_load_dir(model_type=None):
    base_model_name = 'モデル'
    model_type_name = ''

    if model_type is ModelType.COMPARE:
        model_type_name = '比較'

    if model_type is ModelType.REGRESSION:
        model_type_name = '回帰'

    dialog_title = '学習済みの%sをロードするフォルダを選択してください' \
        % (model_type_name+base_model_name)

    load_dir = \
        filedialog.askdirectory(title=dialog_title, initialdir=TRAINDATA_PATH)

    if not load_dir:
        raise FileNotFoundError('フォルダが選択されませんでした')

    return load_dir


class ModelType(Enum):
    COMPARE = auto()
    REGRESSION = auto()


class UseType(Enum):
    TRAINABLE = auto()
    PREDICTABLE = auto()


COMPARE_MODEL_BUILDER_DICT = \
    dict(zip(list(UseType),
             [compare_trainable,  compare_predictable]))

REGRESSION_BUILDER_DICT = \
    dict(zip(list(UseType),
             [regression_trainable,  regression_predictable]))

MODEL_BUILDER_DICT = \
    dict(zip(list(ModelType),
             [COMPARE_MODEL_BUILDER_DICT, REGRESSION_BUILDER_DICT]))


def select_model_type():
    is_use_compare = messagebox.askyesno('modelの選択', 'はいなら比較、いいえなら回帰')

    model_type = ModelType.COMPARE if is_use_compare else ModelType.REGRESSION

    return model_type
