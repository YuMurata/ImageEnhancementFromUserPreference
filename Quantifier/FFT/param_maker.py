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


def _image_to_score(image: Image.Image, filter_size_rate: float):
    rgb_image = image.split()
    rgb_array = [np.array(x) for x in rgb_image]

    rgb_F = np.fft.fftshift(np.fft.fft2(rgb_array))
    rgb_magnitude = 20*np.log(np.abs(rgb_F))

    return sum([_objective_function(magnitude, filter_size_rate)
                for magnitude in rgb_magnitude])


def _objective_function(magnitude: np.array, filter_size_rate: float):
    high_pass_filter = np.ones(magnitude.shape)
    height, width = magnitude.shape
    center_height, center_width = height//2, width//2

    filter_height = int(center_height*filter_size_rate/2)
    filter_width = int(center_width*filter_size_rate/2)

    high_pass_filter[center_height-filter_height:center_height+filter_height,
                     center_width-filter_width:center_width+filter_width] = 0

    return np.sum(magnitude*high_pass_filter)


def _get_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--image_path', required=True)
    parser.add_argument('-s', '--save_file_path', required=True)
    parser.add_argument('-n', '--generate_num', required=True, type=int)
    parser.add_argument('-f', '--filter_size_rate', required=True, type=float)

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

    enhancer = ImageEnhancer(args.image_path)

    game = TournamentGame(image_param_list, handler=stream_handler)

    while not game.is_complete:
        left_param, right_param = game.new_match()

        left_image = enhancer.org_enhance(left_param)
        left_score = _image_to_score(left_image, args.filter_size_rate)

        right_image = enhancer.org_enhance(right_param)
        right_score = _image_to_score(right_image, args.filter_size_rate)

        winner = GameWin.LEFT if left_score > right_score else GameWin.RIGHT
        game.compete(winner)

    write_scored_param(game.scored_player_list, args.save_file_path)
    print(max(game.scored_player_list, key=lambda x:x['score']))
