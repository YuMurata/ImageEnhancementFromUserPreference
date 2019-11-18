from argparse import ArgumentParser
from ParameterOptimizer.main import optimize, show_optimized_images
from ImageEnhancer.image_enhancer import ImageEnhancer
from config.path import root_optimize_dir_path, root_image_dir_path
from misc import get_save_dir_path, Path, get_save_file_path
import matplotlib.pyplot as plt
import json


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-l', '--model_load_dir_path', required=True)
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

    enhancer = ImageEnhancer(str(image_path))
    best_param_list, logbook = optimize(
        args.model_load_dir_path, 'compare', enhancer, 100)

    log_dir_path = Path(optimize_dir_path)/'log'
    log_dir_path.mkdir(exist_ok=True, parents=True)

    make_log(logbook, str(log_dir_path))

    log_file_path = get_save_file_path(log_dir_path, 'fitness.json')
    make_graph(log_file_path, str(log_dir_path))

    show_optimized_images(enhancer, best_param_list, optimize_dir_path)
