from tkinter import Frame, LEFT, StringVar, Label, BOTTOM
from .frame import KeyPressableFrame, CompareCanvasFrame
from .game import TournamentGame, GameWin
import logging


class CompareCanvasGroupFrame(KeyPressableFrame):
    def __init__(self, master: Frame, game: TournamentGame, *, data_writer_list=[]):
        super(CompareCanvasGroupFrame, self).__init__(master)
        self.canvas_width = 300
        self.canvas_height = 300

        self.left_canvas = \
            CompareCanvasFrame(self, self.canvas_width, self.canvas_height)
        self.right_canvas = \
            CompareCanvasFrame(self, self.canvas_width, self.canvas_height)

        self.left_canvas.pack(side=LEFT)
        self.right_canvas.pack(side=LEFT)
        self.select_num_value = StringVar(self)
        Label(self, textvariable=self.select_num_value) \
            .pack(side=BOTTOM)

        self.bind(self.LEFT_PRESS, self._select_left, '+')
        self.bind(self.RIGHT_PRESS, self._select_right, '+')

        self.game = game
        self.data_writer_list = data_writer_list

        self.select_num_value.set(f'残り選択回数: {self.game.get_match_num}')

        self.logger = logging.getLogger('ComparaCanvas')
        self.logger.setLevel(logging.INFO)

        self.focus_set()

    def disp_enhanced_image(self):
        left_image, right_image = self.game.new_match()

        self.left_canvas.canvas.update_image(left_image)
        self.right_canvas.canvas.update_image(right_image)

        self.logger.debug('disp')

    def _select_left(self, e):
        self.logger.debug('press left')
        if self.is_left_press:
            self.logger.debug('hold left')
            return

        self.is_left_press = True
        self.game.compete(GameWin.LEFT)

        self._select_any()

    def _select_right(self, e):
        self.logger.debug('press right')
        if self.is_right_press:
            self.logger.debug('hold right')
            return

        self.is_right_press = True

        self.game.compete(GameWin.RIGHT)

        self._select_any()

    def _select_any(self):
        self.select_num_value.set(f'残り選択回数: {self.game.get_match_num}')
        if self.game.is_complete:
            for data_writer in self.data_writer_list:
                data_writer.write(self.game.scored_player_list)

            self.master.destroy()
        else:
            self.disp_enhanced_image()
