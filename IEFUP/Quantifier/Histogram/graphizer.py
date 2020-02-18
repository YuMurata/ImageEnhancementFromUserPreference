from argparse import ArgumentParser
from ImageEnhancer.image_enhancer import ImageEnhancer
from ScoredParamIO.scored_param_reader import read_scored_param
import matplotlib.pyplot as plt
import numpy as np


def _make_ax(ax, histogram: list, color: str):
    x = [i for i in range(len(histogram))]
    ax.bar(x, histogram)
    ax.set_title(color)
    ax.set_xlabel('brightness')
    ax.tick_params(labelleft="off", left="off")
    return ax


def make_histogram_figure(title: str, histogram_list: list):
    fig = plt.figure(figsize=(18, 4))
    fig.suptitle(title)

    color_list = ['red', 'green', 'blue']
    for i, (histogram, color) in enumerate(zip(histogram_list, color_list)):
        ax = fig.add_subplot(1, 3, i+1)
        _make_ax(ax, histogram.tolist(), color)


def make_image_figure(title: str, image):
    fig, ax = plt.subplots()
    fig.canvas.set_window_title(title)

    ax.imshow(image)
    ax.tick_params(labelbottom="off", bottom="off")  # x軸の削除
    ax.tick_params(labelleft="off", left="off")


def _get_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--image_path', required=True)
    parser.add_argument('-p', '--param_file_path', required=True)

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


if __name__ == "__main__":
    args = _get_args()
    enhancer = ImageEnhancer(args.image_path)
    param_list = read_scored_param(args.param_file_path)

    max_score_param = max(param_list, key=lambda x: x['score'])
    max_score_image = enhancer.org_enhance(max_score_param)
    make_histogram_figure('max', np.array_split(
        max_score_image.histogram(), 3))
    make_image_figure('max', max_score_image)

    min_score_param = min(param_list, key=lambda x: x['score'])
    min_score_image = enhancer.org_enhance(min_score_param)
    make_histogram_figure('min', np.array_split(
        min_score_image.histogram(), 3))
    make_image_figure('min', min_score_image)

    param = {key: 1 for key in min_score_param.keys()}
    org_image = enhancer.org_enhance(param)
    make_histogram_figure('original', np.array_split(
        org_image.histogram(), 3))
    make_image_figure('original', org_image)

    plt.show()
