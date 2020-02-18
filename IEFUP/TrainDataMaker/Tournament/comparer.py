from tkinter import Frame, LEFT, StringVar, Label, BOTTOM
from .frame import KeyPressableFrame, CompareCanvasFrame, LikeButton, KeyInfo
from UserPreferencePredictor.TrainDataMaker import Tournament, GameWin, CompleteException
from UserPreferencePredictor.TrainDataMaker.DataWriter import DataWriter
import logging
import typing


class CompareCanvasGroupFrame(KeyPressableFrame):
    def __init__(self, master: Frame, game: Tournament, *,
                 data_writer_list: typing.List[DataWriter] = [],
                 handler: logging.StreamHandler = None):
        super(CompareCanvasGroupFrame, self).__init__(master)

        self.canvas_width = 300
        self.canvas_height = 300

        self.game = game
        self.data_writer_list = data_writer_list

        self.logger = logging.getLogger('CompareCanvas')
        self.logger.setLevel(logging.INFO)

        if handler is None:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

        self.left_canvas = \
            CompareCanvasFrame(self, self.left_key_info,
                               self.canvas_width, self.canvas_height)

        self.right_canvas = \
            CompareCanvasFrame(self, self.right_key_info,
                               self.canvas_width, self.canvas_height)

        both_button_frame = Frame(self)
        both_win_button = LikeButton(both_button_frame, self.bw_key_info)
        both_win_button.pack()
        both_lose_button = LikeButton(both_button_frame, self.bl_key_info)
        both_lose_button.pack()

        self.left_canvas.pack(side=LEFT)
        both_button_frame.pack(side=LEFT)
        self.right_canvas.pack(side=LEFT)
        self.select_num_value = StringVar(self)
        Label(self, textvariable=self.select_num_value) \
            .pack(side=BOTTOM)

        win_dict = {
            self.LEFT_WIN_KEY_CONFIG.key: GameWin.LEFT,
            self.RIGHT_WIN_KEY_CONFIG.key: GameWin.RIGHT,
            self.BOTH_WIN_KEY_CONFIG.key: GameWin.BOTH_WIN,
            self.BOTH_LOSE_KEY_CONFIG.key: GameWin.BOTH_LOSE,
        }

        def key_press(key_info_: KeyInfo):
            key_config = key_info_.key_config
            self.logger.debug(f'press {key_config.key_type}')
            if self.is_press_any:
                self.logger.debug('hold any key')
                return

            key_info_.is_press = True
            self.game.compete(win_dict[key_config.key])

            self.select_num_value.set(f'残り選択回数: {self.game.get_match_num}')
            if self.game.is_complete:
                self._complete()
            else:
                self.update_image()

        self.bind(self.left_key_info.sequence.press,
                  lambda e: key_press(self.left_key_info), '+')
        self.bind(self.right_key_info.sequence.press,
                  lambda e: key_press(self.right_key_info), '+')
        self.bind(self.bw_key_info.sequence.press,
                  lambda e: key_press(self.bw_key_info), '+')
        self.bind(self.bl_key_info.sequence.press,
                  lambda e: key_press(self.bl_key_info), '+')

        self.select_num_value.set(f'残り選択回数: {self.game.get_match_num}')

        self.focus_set()

    def update_image(self):
        try:
            left_player, right_player = self.game.new_match()
        except CompleteException:
            self._complete()
            return

        left_image, right_image = left_player.decode(), right_player.decode()

        self.left_canvas.canvas.update_image(left_image)
        self.right_canvas.canvas.update_image(right_image)

        self.logger.debug('update')

    def _complete(self):
        for data_writer in self.data_writer_list:
            data_writer.write(self.game.player_list)

        self.master.destroy()