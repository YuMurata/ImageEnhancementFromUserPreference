from enum import Enum, auto
from random import sample
from logging import getLogger, ERROR


class GameException(Exception):
    pass


class GameWin(Enum):
    LEFT = auto()
    RIGHT = auto()


class TournamentGame:
    def __init__(self, player_list: list):
        self.logger = getLogger('Tournament')
        self.logger.setLevel(ERROR)

        self.scored_player_list = [
            {'score': 1, 'param': player} for player in player_list]

        self.current_player_index_list = list(range(len(player_list)))

        self.current_player_index_list = \
            sample(self.current_player_index_list,
                   len(self.current_player_index_list))

        self.next_player_index_list = []

        self.is_match = False
        self.is_complete = False

        self.round_count = 1
        self.match_count = 0

        self.logger.debug('init')
        self.logger.info(f'start {self.round_count}th round')

    def new_match(self):
        if self.is_match:
            raise GameException('match is already ready')

        if self.is_complete:
            raise GameException('game is already over')

        if len(self.current_player_index_list) >= 2:
            self.left_player_index = self.current_player_index_list.pop()
            self.right_player_index = self.current_player_index_list.pop()
            self.is_match = True

            self.match_count += 1
            self.logger.info(
                f'start {self.round_count}-{self.match_count}th match')

            left_player = \
                self.scored_player_list[self.left_player_index]['param']
            right_player = \
                self.scored_player_list[self.right_player_index]['param']

            self.logger.debug(f'left player: {left_player}')
            self.logger.debug(f'right player: {right_player}')
            return left_player, right_player

        else:
            self.next_player_index_list.extend(self.current_player_index_list)
            self.current_player_index_list = \
                sample(self.next_player_index_list,
                       len(self.next_player_index_list))
            self.next_player_index_list.clear()
            self.round_count += 1
            self.match_count = 0

            self.logger.info(f'start {self.round_count}th round')
            return self.new_match()

    def compete(self, winner: GameWin):
        if not self.is_match:
            raise GameException('match is not ready yet')

        if self.is_complete:
            raise GameException('game is already over')

        if winner == GameWin.LEFT:
            self.scored_player_list[self.left_player_index]['score'] *= 2
            self.next_player_index_list.append(self.left_player_index)
        else:
            self.scored_player_list[self.right_player_index]['score']
            self.next_player_index_list.append(self.right_player_index)

        self.logger.info(f'winner: {winner.name}')
        self.is_match = False

        is_no_current_player = len(self.current_player_index_list) == 0
        is_only_one_winner = len(self.next_player_index_list) == 1

        if is_no_current_player and is_only_one_winner:
            self.is_complete = True

    @property
    def get_match_num(self):
        current_match_num = len(self.current_player_index_list)
        next_match_num = len(self.next_player_index_list)
        return current_match_num+next_match_num
