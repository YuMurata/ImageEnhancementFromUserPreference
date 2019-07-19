from ImageEnhancer.enhance_definer import enhance_name_list
from TrainDataGenerator.tournament.game import TournamentGame, GameWin
from TrainDataGenerator.image_parameter_generator \
    import generate_image_parameter_list
import numpy as np
from argparse import ArgumentParser
from ScoredParamIO.scored_param_writer import write_scored_param
from pathlib import Path
from logging import StreamHandler


def param_to_score(param: dict, target_param: float):
    score = 0
    for key, value in param.items():
        if key == 'score':
            continue
        score += np.exp(-abs(target_param-value))

    return score


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-o', '--save_file_path', required=True)
    parser.add_argument('-n', '--generate_num', required=True, type=int)
    parser.add_argument('-t', '--target_param', required=True, type=float)

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
    stream_handler = None

    image_param_list = generate_image_parameter_list(enhance_name_list,
                                                     args.generate_num)

    game = TournamentGame(image_param_list, handler=stream_handler)

    while not game.is_complete:
        left_param, right_param = game.new_match()

        left_score = param_to_score(left_param, args.target_param)
        right_score = param_to_score(right_param, args.target_param)

        winner = GameWin.LEFT if left_score > right_score else GameWin.RIGHT
        game.compete(winner)

    write_scored_param(game.scored_player_list, args.save_file_path)
