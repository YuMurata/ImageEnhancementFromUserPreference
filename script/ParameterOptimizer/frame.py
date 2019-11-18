from tkinter import Frame, Button, Toplevel, LEFT
from ImageEnhancer.image_enhancer import ImageEnhancer
from GUI.image_canvas_frame import ImageCanvas
from random import gauss
from pathlib import Path
TARGET_WIDTH = 300


class CanvasGroupFrame(Frame):
    def __init__(self, master, param_list: list, enhancer: ImageEnhancer, save_dir_path: str):
        super(CanvasGroupFrame, self).__init__(master)

        canvas_frame = Frame(self)
        for param in param_list:
            frame = SelectableCanvasFrame(
                canvas_frame, enhancer, param, save_dir_path)
            frame.pack(side=LEFT)
            frame.canvas.update_image(enhancer.org_enhance(param))

        canvas_frame.pack()
        Button(self, text='save', command=self._click_save).pack()

        self.param_list = param_list
        self.enhancer = enhancer
        self.save_dir_path = Path(save_dir_path)
        self.save_dir_path.mkdir(exist_ok=True, parents=True)

    def _click_save(self):
        for index, param in enumerate(self.param_list):
            save_path = str(self.save_dir_path/f'best_{index}.png')
            self.enhancer.org_enhance(param).save(save_path)

        self.winfo_toplevel().destroy()


class SelectableCanvasFrame(Frame):
    def __init__(self, master: Frame, enhancer: ImageEnhancer,
                 enhance_param: dict, save_dir_path: str):

        super(SelectableCanvasFrame, self).__init__(master)

        target_height = \
            int(TARGET_WIDTH/enhancer.org_width*enhancer.org_height)

        self.canvas = ImageCanvas(self, TARGET_WIDTH, target_height)
        self.canvas.pack()
        Button(self, text='good', command=self._click_good).pack()

        self.enhancer = enhancer
        self.enhance_param = enhance_param
        self.save_dir_path = save_dir_path

    def _click_good(self):
        self._param_update(self.enhance_param)

    def _param_update(self, org_enhance_param: dict):
        sub_win = Toplevel(self)
        sub_win.lift()
        sub_win.title('optimizer_sub')

        gauss_param_list = []
        param_key_list = org_enhance_param.keys()
        param_list = org_enhance_param.values()

        mu = 1
        variation_width = 0.5
        sigma = variation_width/3

        disp_num = 4

        for i in range(disp_num):
            gauss_param = \
                [param*gauss(mu, sigma) for param in param_list]

            gauss_param_list.append(
                dict(zip(param_key_list, gauss_param)))

        CanvasGroupFrame(sub_win, gauss_param_list,
                         self.enhancer, self.save_dir_path).pack()
