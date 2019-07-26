from tkinter import Tk, LEFT
from argparse import ArgumentParser
from UserPreferencePredictor.Model.util \
    import MODEL_TYPE_LIST
from UserPreferencePredictor.Model.Compare.ranknet import RankNet

import sys
from ImageEnhancer.image_enhancer import ImageEnhancer

from ParameterOptimizer.optimizer import ParameterOptimizer
from ParameterOptimizer.frame import SelectableCanvasFrame


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-l', '--load_dir_path', required=True)
    parser.add_argument('-i', '--image_path', required=True)
    parser.add_argument('-t', '--model_type', choices=MODEL_TYPE_LIST,
                        required=True)

    return parser.parse_args()


def _init_model(load_dir_path: str, model_type: str):
    model = RankNet()
    try:
        model.load(load_dir_path)
    except ValueError:
        print('学習済みモデルをロードできなかったため終了します')
        sys.exit()

    return model


def _show_histogram(image):
    from Quantifier.Histogram.graphizer \
        import make_histogram_figure, make_image_figure
    import matplotlib.pyplot as plt
    import numpy as np

    make_histogram_figure('histogram', np.array_split(image.histogram(), 3))
    make_image_figure('', image)

    plt.show()


def _show_optimized_images(enhancer: ImageEnhancer, best_param_list: list):
    root = Tk()
    root.title('optimizer')
    for param in best_param_list:
        frame = SelectableCanvasFrame(root, enhancer, param)
        frame.pack(side=LEFT)
        frame.canvas.update_image(image_enhancer.org_enhance(param))

    root.lift()

    root.mainloop()


def _show_identify(enhancer: ImageEnhancer, best_param_list: list):
    print(best_param_list[0])
    from Quantifier.Histogram.graphizer import make_image_figure
    import matplotlib.pyplot as plt
    make_image_figure('', image_enhancer.org_enhance(best_param_list[0]))
    plt.show()


def optimize(load_dir_path: str, model_type: str, enhancer: ImageEnhancer):
    model = _init_model(load_dir_path, model_type)

    optimizer = ParameterOptimizer(model, enhancer)
    best_param_list = optimizer.optimize()
    return best_param_list


if __name__ == "__main__":
    args = _get_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    image_enhancer = ImageEnhancer(args.image_path)
    best_param_list = optimize(**args)

    _show_identify(image_enhancer, best_param_list)
