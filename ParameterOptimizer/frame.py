from tkinter import Frame, Button, Toplevel, LEFT
from ImageEnhancer.image_enhancer import ImageEnhancer
from GUI.image_canvas_frame import ImageCanvas
from random import gauss

TARGET_WIDTH = 300


class SelectableCanvasFrame(Frame):
    def __init__(self, master: Frame, enhancer: ImageEnhancer,
                 enhance_param: dict):

        super(SelectableCanvasFrame, self).__init__(master)

        target_height = \
            int(TARGET_WIDTH/enhancer.org_width*enhancer.org_height)

        self.canvas = ImageCanvas(self, TARGET_WIDTH, target_height)
        self.canvas.pack()
        Button(self, text='good', command=self._click_button).pack()

        self.enhancer = enhancer
        self.enhance_param = enhance_param

    def _click_button(self):
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

        for param in gauss_param_list:
            frame = \
                SelectableCanvasFrame(
                    sub_win, self.enhancer, self.enhance_param)
            frame.pack(side=LEFT)
            frame.canvas.update_image(self.enhancer.org_enhance(param))
