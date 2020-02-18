import tkinter as tk
from tkinter import ttk
from collections import namedtuple
from PIL import Image, ImageTk

KeyConfig = namedtuple('KeyConfig', ['key', 'key_type'])


class ImageCanvas(tk.Canvas):
    def __init__(self, master: ttk.Frame, canvas_width: int,
                 canvas_height: int):

        super(ImageCanvas, self) \
            .__init__(master, width=canvas_width, height=canvas_height)

        self.image_id = \
            self.create_image(canvas_width/2, canvas_height/2)
        self.photo_image = None

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def update_image(self, image: Image.Image):
        resized_image = image.resize((self.canvas_width, self.canvas_height))
        self.photo_image = ImageTk.PhotoImage(resized_image, master=self)

        self.itemconfigure(self.image_id, image=self.photo_image)


class Sequence:
    def __init__(self, key: str):
        self.press = f'<KeyPress-{key}>'
        self.release = f'<KeyRelease-{key}>'


class KeyInfo:
    def __init__(self, key_config: KeyConfig):
        self.key_config = key_config
        self.sequence = Sequence(key_config.key)
        self.is_press = False


class LikeButton(ttk.Button):
    def __init__(self, master, key_info: KeyInfo):
        key_config = key_info.key_config
        super().__init__(master,
                         text=f'like {key_config.key_type}({key_config.key})',
                         width=15,)

        self.key_info = key_info

        def release(e):
            self.key_info.is_press = False
        self.bind('<ButtonRelease-1>', release, '+')


class CompareCanvasFrame(ttk.Frame):
    def __init__(self, master, key_info: KeyInfo,
                 canvas_width: int, canvas_height: int):
        super(CompareCanvasFrame, self).__init__(master)

        self.canvas = ImageCanvas(self, canvas_width, canvas_height)
        self.button = LikeButton(self, key_info)
        self.canvas.pack()
        self.button.pack()


class KeyPressableFrame(ttk.Frame):

    LEFT_WIN_KEY_CONFIG = KeyConfig('f', 'left')
    RIGHT_WIN_KEY_CONFIG = KeyConfig('j', 'right')
    BOTH_WIN_KEY_CONFIG = KeyConfig('g', 'both_win')
    BOTH_LOSE_KEY_CONFIG = KeyConfig('h', 'both_lose')

    def __init__(self, master):
        super(KeyPressableFrame, self).__init__(master)

        self.left_key_info = KeyInfo(self.LEFT_WIN_KEY_CONFIG)
        self.right_key_info = KeyInfo(self.RIGHT_WIN_KEY_CONFIG)
        self.bw_key_info = KeyInfo(self.BOTH_WIN_KEY_CONFIG)
        self.bl_key_info = KeyInfo(self.BOTH_LOSE_KEY_CONFIG)

        self.key_info_list = [key_info
                              for key_info in [self.left_key_info,
                                               self.right_key_info,
                                               self.bw_key_info,
                                               self.bl_key_info]]

        def release(key_info: KeyInfo):
            key_info.is_press = False

        self.bind_all(self.left_key_info.sequence.release,
                      lambda e: release(self.left_key_info), '+')
        self.bind_all(self.right_key_info.sequence.release,
                      lambda e: release(self.right_key_info), '+')
        self.bind_all(self.bw_key_info.sequence.release,
                      lambda e: release(self.bw_key_info), '+')
        self.bind_all(self.bl_key_info.sequence.release,
                      lambda e: release(self.bl_key_info), '+')

    @property
    def is_press_any(self):
        return any([key_info.is_press
                    for key_info in self.key_info_list])
