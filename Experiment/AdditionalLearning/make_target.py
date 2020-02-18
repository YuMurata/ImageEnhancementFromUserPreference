from IEFUP.ImageEnhancer \
    import generate_random_param_list, enhance_name_list, ImageEnhancer
from IEFUP.submodule import Tournament
import json
from pathlib import Path
from logging import StreamHandler, INFO


class ParamPlayer(Tournament.Player):
    def __init__(self, param):
        super().__init__(param)

    def decode(self):
        return self.param


def param_distance(paramA: dict, paramB: dict):
    return sum([abs(paramA[enhance_name] - paramB[enhance_name])
                for enhance_name in enhance_name_list])


def make_param(target):
    return {
        'brightness': target,
        'saturation': target,
        'contrast': target,
        'sharpness': target
    }


if __name__ == "__main__":
    target_dict = {
        'farm': 0.6,
        'flower': 0.8,
        'katsudon': 1.2,
        'waterfall': 1.4,
    }

    generate_num = 100

    handler = StreamHandler()
    handler.setLevel(INFO)
    handler = None

    target_dir = Path(__file__).parent / 'target'
    target_dir.mkdir(exist_ok=True, parents=True)

    trainable_dir = Path(__file__).parent / 'trainable'
    for image_path in trainable_dir.iterdir():
        category_name = image_path.stem
        target_param = make_param(target_dict[category_name])

        player_list = [ParamPlayer(param)
                       for param in generate_random_param_list(generate_num)]

        tournament = Tournament.Tournament(player_list, handler=handler)

        while not tournament.is_complete:
            is_complete, (playerL, playerR) = tournament.new_match()

            if is_complete:
                break

            paramL = playerL.decode()
            paramR = playerR.decode()

            L_to_T = param_distance(paramL, target_param)
            R_to_T = param_distance(paramR, target_param)

            if L_to_T < R_to_T:
                tournament.compete(Tournament.GameWin.LEFT)
            else:
                tournament.compete(Tournament.GameWin.RIGHT)

        scored_param_dict = [player.to_dict() for player in player_list]

        image_name = image_path.stem

        param_dir = target_dir / 'param'
        param_dir.mkdir(exist_ok=True)
        with open(str(param_dir / f'{image_name}.json'), 'w') as fp:
            json.dump(scored_param_dict, fp)

        best_param = \
            sorted(scored_param_dict, key=lambda x: x['score'])[-1]['param']

        print(f'target_param: {target_param} in {image_name}')
        print(f'best_param: {best_param} in {image_name}')

        # enhancer = ImageEnhancer(str(image_path))

        # image_dir = target_dir / 'image'
        # image_dir.mkdir(exist_ok=True)
        # enhancer.enhance(best_param).save(
        #     str(image_dir / f'{image_name}.png'))
