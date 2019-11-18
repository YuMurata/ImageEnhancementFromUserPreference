from argparse import ArgumentParser
from ImageEnhancer.image_enhancer import ImageEnhancer
from config.path import root_image_dir_path, root_manual_dir_path
from datetime import datetime

import tkinter as tk
from tkinter import ttk
from ImageEnhancer.enhance_definer import enhance_name_list
from GUI.image_canvas_frame import ImageCanvas
from TrainDataGenerator.image_parameter_generator import MAX_PARAM, MIN_PARAM
from pathlib import Path


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-i', '--image_name', required=True)
    parser.add_argument('-n', '--image_number', required=True)
    parser.add_argument('-u', '--user_name', required=True)

    args = parser.parse_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


class Drawer:
    def __init__(self, enhancer: ImageEnhancer, canvas: ImageCanvas):
        self.enhancer = enhancer
        self.canvas = canvas
        self.enhance_param = {
            param_name: 1 for param_name in enhance_name_list}

    def update_param(self, param_name: str, value: float):
        self.enhance_param[param_name] = value

    def update_image(self):
        self.canvas.update_image(self.enhancer.org_enhance(self.enhance_param))

    def save_image(self, save_dir_path: str):
        save_dir_path = Path(save_dir_path)
        save_dir_path.mkdir(exist_ok=True, parents=True)

        self.enhancer.org_enhance(self.enhance_param).save(
            str(save_dir_path/'manual_enhancement.png'))


class ParamController(ttk.Frame):
    def __init__(self, master, param_name: str, drawer: Drawer):
        super(ParamController, self).__init__(master)
        self.param_name = param_name
        self.drawer = drawer

        self.value = tk.DoubleVar(self, value=1)
        self.value.trace('w', self._value_trace)

        label_frame = ttk.Frame(self)
        self.label_var = tk.StringVar(label_frame, value=self.value.get())
        ttk.Label(label_frame, text=param_name).pack(side=tk.LEFT)
        ttk.Label(label_frame, textvariable=self.label_var).pack(side=tk.LEFT)
        label_frame.pack()

        ttk.Scale(self, variable=self.value,
                  orient=tk.HORIZONTAL, from_=MIN_PARAM, to=MAX_PARAM).pack()

    def _value_trace(self, *args):
        value = self.value.get()
        self.label_var.set(f'{value:.2f}')
        self.drawer.update_param(self.param_name, value)
        self.drawer.update_image()


if __name__ == "__main__":
    args = _get_args()

    root = tk.Tk()

    image_path = \
        list((root_image_dir_path/args.image_name /
              'original').glob(f'{args.image_number}.*'))[0]

    now = datetime.now()
    date = '{0:%m%d}'.format(now)
    time = '{0:%H%M}'.format(now)
    save_dir_path = root_manual_dir_path/args.user_name / \
        args.image_name/args.image_number/date/time
    save_dir_path.mkdir(parents=True, exist_ok=True)

    enhancer = ImageEnhancer(str(image_path))

    def canvas_creation():
        canvas = ImageCanvas(root, enhancer.org_width, enhancer.org_width)
        canvas.pack()
        return canvas

    canvas = canvas_creation()

    drawer = Drawer(enhancer, canvas)
    drawer.update_image()

    def click_save():
        drawer.save_image(str(save_dir_path))
        root.destroy()

    def ui_frame_creation():
        ui_frame = ttk.Frame(root)

        def param_controller_creation():
            param_controller_frame = ttk.Frame(ui_frame)
            for enhance_name in enhance_name_list:
                ParamController(param_controller_frame,
                                enhance_name, drawer).pack()
            param_controller_frame.pack(side=tk.LEFT)

        param_controller_creation()

        ttk.Button(ui_frame, text='save', command=click_save).pack(side=tk.LEFT)

        ui_frame.pack()

    ui_frame_creation()

    root.mainloop()
