from argparse import ArgumentParser
from UserPreferencePredictor.Model import RankNet
from UserPreferencePredictor.PreferenceOptimizer import Optimizer
from IEFUP.ImageEnhancer import ResizableEnhancer
from config.path import root_optimize_dir_path, root_image_dir_path
from config.dataset import IMAGE_SHAPE, IMAGE_SIZE
from misc import get_save_dir_path, Path, get_save_file_path
from IEFUP.Optimize import EnhanceGenerator, EnhanceDecorder
import matplotlib.pyplot as plt
import json
from pathlib import Path


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-w', '--weights_file_path', required=True)
    parser.add_argument('-i', '--image_name', required=True)
    parser.add_argument('-n', '--image_number', required=True)
    parser.add_argument('-u', '--user_name', required=True)

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


def make_log(logbook, log_dir_path: str):
    field_name_list = ['gen', 'avg', 'min', 'max']
    log_dict = {key: value for key, value in zip(
        field_name_list, logbook.select(*field_name_list))}

    log_file_path = get_save_file_path(log_dir_path, 'fitness.json')
    with open(log_file_path, 'w') as fp:
        json.dump(log_dict, fp, indent=4)


def make_graph(log_file_path: str, log_dir_path: str):
    with open(log_file_path, 'r') as fp:
        log_dict = json.load(fp)

    fig, ax1 = plt.subplots()

    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness")

    ax1.plot(log_dict['gen'], log_dict['avg'],
             color='r', label="Average Fitness")
    ax1.plot(log_dict['gen'], log_dict['min'],
             color='g', label="Minimum Fitness")
    ax1.plot(log_dict['gen'], log_dict['max'],
             color='b', label="Maximum Fitness")

    ax1.legend()

    save_file_path = get_save_file_path(log_dir_path, 'graph.png')
    plt.savefig(str(save_file_path))


if __name__ == "__main__":
    args = _get_args()

    optimize_dir_path = get_save_dir_path(
        root_optimize_dir_path, args.user_name, f'{args.image_name}/{args.image_number}')

    image_dir = root_image_dir_path/args.image_name/args.image_number
    image_path = list(image_dir.glob('*.*'))[0]

    enhancer = ResizableEnhancer(str(image_path), IMAGE_SIZE)

    model = RankNet(IMAGE_SHAPE)
    model.load(args.weights_file_path)
    image_generator = EnhanceGenerator(enhancer)
    best_param_list, _ = Optimizer(model, image_generator, EnhanceDecorder()).optimize(20)

    for index, best_param in enumerate(best_param_list):
        save_path = str(Path(optimize_dir_path)/f'best_{index}.png')
        enhancer.enhance(best_param).save(save_path)
