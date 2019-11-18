from enum import Enum, auto
from random import sample
from logging import getLogger, INFO
from tqdm import tqdm
from TrainDataGenerator.data_generator import DataGenerator


class GameException(Exception):
    pass


class GameWin(Enum):
    LEFT = auto()
    RIGHT = auto()


class TournamentGame:
    def __init__(self, param_list: list, generator: DataGenerator, *, handler=None):
        self.logger = getLogger('Tournament')
        self.logger.setLevel(INFO)

        if handler is not None:
            self.logger.addHandler(handler)

        self.player_list = [generator.generate(param) for param in tqdm(param_list, desc='generate image')]
        self.scored_player_list = [
            {'score': 1, 'player': player, 'param': param} for player, param in zip(self.player_list, param_list)]
        self.current_player_index_list = list(range(len(param_list)))

        self.current_player_index_list = \
            sample(self.current_player_index_list,
                   len(self.current_player_index_list))

        self.next_player_index_list = []

        self.is_match = False
        self.is_complete = False

        self.round_count = 1
        self.match_count = 0

        self.logger.debug('init')

        self.logger.info(f'--- game start ---')

        self.logger.info(f'start {self.round_count}th round')
        self.logger.info(
            f'--- current player: {self.current_player_index_list} ---')
        score_list = [player['score']
                      for player in self.scored_player_list]
        self.logger.info(f'--- score: {score_list} ---')

    def _new_round(self):
        if len(self.current_player_index_list) >= 2:
            raise GameException

        for index in self.current_player_index_list:
            self.scored_player_list[index]['score'] *= 2

        self.next_player_index_list.extend(self.current_player_index_list)
        self.current_player_index_list = \
            sample(self.next_player_index_list,
                   len(self.next_player_index_list))
        self.next_player_index_list.clear()

        self.round_count += 1
        self.match_count = 0

        self.logger.info(f'start {self.round_count}th round')
        self.logger.info(
            f'--- current player: {self.current_player_index_list} ---')
        score_list = [player['score']
                      for player in self.scored_player_list]
        self.logger.info(f'--- score: {score_list} ---')

    def new_match(self):
        if self.is_match:
            raise GameException('match is already ready')

        if self.is_complete:
            raise GameException('game is already over')

        self.logger.info(f'--- new match start ---')

        if len(self.current_player_index_list) >= 2:
            self.left_player_index = self.current_player_index_list.pop()
            self.right_player_index = self.current_player_index_list.pop()
            self.is_match = True

            self.match_count += 1

            left_player = \
                self.player_list[self.left_player_index]
            right_player = \
                self.player_list[self.right_player_index]

            self.logger.info(
                f'--- left player: {self.left_player_index} ---')
            self.logger.info(
                f'--- right player: {self.right_player_index} ---')

            return left_player, right_player

        else:
            self._new_round()
            return self.new_match()

    def compete(self, winner: GameWin):
        if not self.is_match:
            raise GameException('match is not ready yet')

        if self.is_complete:
            raise GameException('game is already over')

        winner_index = self.left_player_index \
            if winner == GameWin.LEFT else \
            self.right_player_index

        self.scored_player_list[winner_index]['score'] *= 2
        self.next_player_index_list.append(winner_index)

        self.logger.info(f'--- winner: {winner.name} ---')
        self.is_match = False

        is_no_current_player = len(self.current_player_index_list) == 0
        is_only_one_winner = len(self.next_player_index_list) == 1

        if is_no_current_player and is_only_one_winner:
            self.is_complete = True

    @property
    def get_match_num(self):
        current_match_num = len(self.current_player_index_list)-1
        next_match_num = len(self.next_player_index_list)
        return current_match_num+next_match_num
