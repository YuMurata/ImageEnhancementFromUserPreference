from IEFUP.TrainDataMaker.generate_param import generate_random_param_list
from UserPreferencePredictor.TrainDataMaker.Tournament import TournamentGame, GameWin, Player
import typing
from IEFUP.ImageEnhancer import enhance_name_list


class ParamPlayer(Player):
    def __init__(self, param: dict):
        super(ParamPlayer, self).__init__(param)

    def decode(self):
        return self.param


def tournament(compare_num: int, target_param_dict: dict) -> typing.List[Player]:
    def _score(param: dict):
        return -sum([abs(param[enhance_name]-target_param_dict[enhance_name]) for enhance_name in enhance_name_list])

    player_list = [ParamPlayer(param)
                   for param in generate_random_param_list(compare_num)]
    game = TournamentGame(player_list)

    while not game.is_complete:
        left, right = game.new_match()
        if _score(left.param) > _score(right.param):
            game.compete(GameWin.LEFT)
        else:
            game.compete(GameWin.RIGHT)

    return game.player_list
