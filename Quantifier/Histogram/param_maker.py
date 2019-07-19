from ImageEnhancer.image_enhancer import ImageEnhancer, Image
from ImageEnhancer.enhance_definer import enhance_name_list
from TrainDataGenerator.tournament.game import TournamentGame, GameWin
from TrainDataGenerator.image_parameter_generator \
    import generate_image_parameter_list
import numpy as np
from argparse import ArgumentParser
from ScoredParamIO.scored_param_writer import write_scored_param
from pathlib import Path
from logging import StreamHandler


def _image_to_score(image: Image.Image, target_tuple: tuple):

    histogram_list = np.array_split(image.histogram(), 3)
    return sum([_objective_function(histogram, target)
                for histogram, target in zip(histogram_list, target_tuple)])


def _objective_function(histogram_list: list, target: int):
    target_diff = np.abs([x - target for x in range(len(histogram_list))])
    sum_histogram = np.sum(histogram_list)
    return np.sum(np.array(histogram_list)/np.exp(target_diff))/sum_histogram


def _get_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--image_path', required=True)
    parser.add_argument('-s', '--save_file_path', required=True)
    parser.add_argument('-n', '--generate_num', required=True, type=int)
    parser.add_argument('-r', '--target_red', required=True, type=int)
    parser.add_argument('-g', '--target_green', required=True, type=int)
    parser.add_argument('-b', '--target_blue', required=True, type=int)

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


if __name__ == "__main__":
    args = _get_args()
    if args.generate_num < 2:
        raise ValueError('生成数は2以上にしてください')

    if not Path(args.save_file_path).parent.exists():
        raise ValueError('フォルダが存在しません')

    if Path(args.save_file_path).suffix != '.csv':
        raise ValueError('拡張子はcsvにしてください')

    stream_handler = StreamHandler()

    image_param_list = generate_image_parameter_list(enhance_name_list,
                                                     args.generate_num)

    target_tuple = (args.target_red, args.target_green, args.target_blue)
    enhancer = ImageEnhancer(args.image_path)

    game = TournamentGame(image_param_list)

    while not game.is_complete:
        left_param, right_param = game.new_match()

        left_image = enhancer.resized_enhance(left_param)
        left_score = _image_to_score(left_image, target_tuple)

        right_image = enhancer.resized_enhance(right_param)
        right_score = _image_to_score(right_image, target_tuple)

        winner = GameWin.LEFT if left_score > right_score else GameWin.RIGHT
        game.compete(winner)

    write_scored_param(game.scored_player_list, args.save_file_path)
