from IEFUP.ImageEnhancer import ResizableEnhancer, enhance_name_list
import config
from IEFUP.TrainDataMaker.generate_param import generate_random_param_list
from IEFUP.TrainDataMaker.new_records import TFRecordsWriter, SUFFIX
from pathlib import Path
from UserPreferencePredictor.TrainDataMaker.Tournament import TournamentGame, GameWin, Player, Evaluator


def _param_diff(param, target_param):
    return -sum([abs(param[enhance_name]-target_param[enhance_name]) for enhance_name in enhance_name_list])


def _score(param: dict):
    return -sum([abs(param[enhance_name]-config.target_param_dict[enhance_name]) for enhance_name in enhance_name_list])


def _tournament(compare_num: int) -> Evaluator:
    player_list = [ParamPlayer(param)
                   for param in generate_random_param_list(compare_num)]
    game = TournamentGame(player_list)

    while not game.is_complete:
        left, right = game.new_match()
        if _score(left.param) > _score(right.param):
            game.compete(GameWin.LEFT)
        else:
            game.compete(GameWin.RIGHT)

    return Evaluator(game.player_list, _param_diff)


def _write(enhancer: ResizableEnhancer, compare_num: int, generate_num: int, save_dir_path: Path, dataset_type: str):
    evaluator = _tournament(compare_num)
    save_file_path = str(save_dir_path/f'{dataset_type}{SUFFIX}')
    writer = TFRecordsWriter(save_file_path)
    writer.write(enhancer, evaluator, generate_num)


class ParamPlayer(Player):
    def __init__(self, param: dict):
        super(ParamPlayer, self).__init__(param)
        self.enhancer = enhancer

    def decode(self):
        return self.param


if __name__ == "__main__":
    tfrecords_dir_path = Path(
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\VGG16_Change_DataNum\new_tfrecords')

    compare_num = 100
    generate_num_list = [4000]
    enhancer = ResizableEnhancer(
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\katsudon\1\1.jpg', config.IMAGE_SIZE)

    for generate_num in generate_num_list:
        save_dir_path = tfrecords_dir_path/str(generate_num)
        save_dir_path.mkdir(exist_ok=True, parents=True)

        _write(enhancer, compare_num, generate_num, save_dir_path, 'train')
        _write(enhancer, compare_num//10, generate_num //
               10, save_dir_path, 'validation')
