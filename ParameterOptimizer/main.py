from tkinter import Tk, LEFT
from argparse import ArgumentParser
from UserPreferencePredictor.Model.util \
    import MODEL_TYPE_LIST, MODEL_BUILDER_DICT, PREDICTABLE
import sys
from ImageEnhancer.image_enhancer import ImageEnhancer

from ParameterOptimizer.optimizer import ParameterOptimizer
from ParameterOptimizer.frame import SelectableCanvasFrame
import tensorflow as tf


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-l', '--load_dir_path', required=True)
    parser.add_argument('-i', '--image_path', required=True)
    parser.add_argument('-t', '--model_type', choices=MODEL_TYPE_LIST,
                        required=True)

    return parser.parse_args()


def _init_model(load_dir_path: str, model_type: str):
    model = MODEL_BUILDER_DICT[model_type][PREDICTABLE](tf.Graph())
    try:
        model.restore(load_dir_path)
    except ValueError:
        print('学習済みモデルをロードできなかったため終了します')
        sys.exit()

    return model


if __name__ == "__main__":
    args = _get_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    model = _init_model(args.load_dir_path, args.model_type)
    image_enhancer = ImageEnhancer(args.image_path)

    optimizer = ParameterOptimizer(model, image_enhancer)
    best_param_list = optimizer.optimize()

    root = Tk()
    root.title('optimizer')
    for param in best_param_list:
        frame = SelectableCanvasFrame(root, image_enhancer, param)
        frame.pack(side=LEFT)
        frame.canvas.update_image(image_enhancer.org_enhance(param))

    root.lift()

    root.mainloop()
