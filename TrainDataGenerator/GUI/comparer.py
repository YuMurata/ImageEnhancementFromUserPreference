import csv

from tkinter import filedialog, Frame, LEFT, Button, BOTTOM, Label, StringVar

from ImageEnhancer.image_enhancer import ImageEnhancer
from TrainDataGenerator.image_parameter_generator \
    import generate_image_parameter_list
from ImageEnhancer.enhance_definer import enhance_name_list

from GUI.image_canvas_frame import ImageCanvas

from random import sample as random_sample
from ScoredParamIO.scored_param_writer import write_scored_param


class CompareCanvasFrame(Frame):
    def __init__(self, master: Frame,
                 canvas_width: int, canvas_height: int):
        super(CompareCanvasFrame, self).__init__(master)

        self.canvas = ImageCanvas(self, canvas_width, canvas_height)
        self.button = Button(self, text='good', width=6,)
        self.canvas.pack()
        self.button.pack()


class KeyPressableFrame(Frame):
    LEFT_KEY = 'f'
    RIGHT_KEY = 'j'

    LEFT_PRESS = f'<KeyPress-{LEFT_KEY}>'
    RIGHT_PRESS = f'<KeyPress-{RIGHT_KEY}>'

    LEFT_RELEASE = f'<KeyRelease-{LEFT_KEY}>'
    RIGHT_RELEASE = f'<KeyRelease-{RIGHT_KEY}>'

    def __init__(self, master: Frame):
        super(KeyPressableFrame, self).__init__(master)

        self.is_left_press = False
        self.is_right_press = False

        self.bind_all(self.LEFT_RELEASE, self._release_left, '+')
        self.bind_all(self.RIGHT_RELEASE, self._release_right, '+')

    def _release_left(self, e):
        self.is_left_press = False

    def _release_right(self, e):
        self.is_right_press = False


class CompareCanvasGroupFrame(KeyPressableFrame):
    def __init__(self, master: Frame):
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
        self.select_num_value.set('残り選択回数: ---')
        Label(self, textvariable=self.select_num_value) \
            .pack(side=BOTTOM)

        self.bind_all(self.LEFT_PRESS, self._click_left_canvas, '+')
        self.bind_all(self.RIGHT_PRESS, self._click_right_canvas, '+')

    def make_image_generator(self, image_enhancer: ImageEnhancer,
                             generate_num: int):
        self.image_enhancer = image_enhancer
        self.image_parameter_list = \
            generate_image_parameter_list(enhance_name_list, generate_num)
        self.scored_param_list = \
            [{'score': 1, 'param': image_param}
             for image_param in self.image_parameter_list]
        self.current_image_parameter_index_list = \
            random_sample(
                [i for i in range(generate_num)], generate_num)
        self.next_image_parameter_index_list = []

        self.select_num_value.set('残り選択回数: %i' % (
            len(self.current_image_parameter_index_list) +
            len(self.next_image_parameter_index_list)))

    def disp_enhanced_image(self):
        self.left_image_parameter_index = \
            self.current_image_parameter_index_list.pop()
        self.right_image_parameter_index = \
            self.current_image_parameter_index_list.pop()

        left_image_parameter = \
            self.image_parameter_list[self.left_image_parameter_index]
        right_image_parameter = \
            self.image_parameter_list[self.right_image_parameter_index]

        left_enhanced_image = \
            self.image_enhancer.org_enhance(left_image_parameter)
        right_enhanced_image = \
            self.image_enhancer.org_enhance(right_image_parameter)

        self.left_canvas.canvas.update_image(left_enhanced_image)
        self.right_canvas.canvas.update_image(right_enhanced_image)

        self.focus_set()

    def _click_left_canvas(self, e):
        if self.is_left_press:
            return

        self.is_left_press = True

        selected_index = self.left_image_parameter_index
        selected_score = \
            self.scored_param_list[self.left_image_parameter_index]['score']
        other_score = \
            self.scored_param_list[self.right_image_parameter_index]['score']

        self.next_image_parameter_index_list.append(
            self.left_image_parameter_index)
        self.select_num_value.set('残り選択回数: %i' % (
            len(self.current_image_parameter_index_list) +
            len(self.next_image_parameter_index_list)))
        self._tournament(selected_index, selected_score, other_score)

    def _click_right_canvas(self, e):
        if self.is_right_press:
            return

        self.is_right_press = True

        selected_index = self.right_image_parameter_index
        selected_score = \
            self.scored_param_list[self.right_image_parameter_index]['score']
        other_score = \
            self.scored_param_list[self.left_image_parameter_index]['score']

        self.next_image_parameter_index_list.append(
            self.right_image_parameter_index)
        self.select_num_value.set('残り選択回数: %i' % (
            len(self.current_image_parameter_index_list) +
            len(self.next_image_parameter_index_list)))
        self._tournament(selected_index, selected_score, other_score)

    def _scored_tournament(self, selected_index: int):
        self.scored_param_list[selected_index]['score'] *= 2

    def _scored_competition(self, selected_index: int, selected_score: int,
                            other_score: int):
        if selected_score <= other_score:
            self.scored_param_list[selected_index]['score'] = other_score
            for index in range(len(self.scored_param_list)):
                if index == selected_index:
                    continue

                scored_param = self.scored_param_list[index]
                if selected_score <= scored_param['score'] <= other_score:
                    scored_param['score'] -= 1

    def _tournament(self, selected_index: int, selected_score: int,
                    other_score: int):
        self._scored_tournament(selected_index)

        if len(self.current_image_parameter_index_list) < 2:
            if len(self.current_image_parameter_index_list) == 0 and\
                    len(self.next_image_parameter_index_list) == 1:
                print('tournament complete')
                write_scored_param(self.scored_param_list)
                # self._write_scored_parameter_to_csv()
                self.master.destroy()
                return

            self.next_image_parameter_index_list.extend(
                self.current_image_parameter_index_list)

            self.current_image_parameter_index_list = random_sample(
                self.next_image_parameter_index_list,
                len(self.next_image_parameter_index_list))

            self.next_image_parameter_index_list.clear()

        self.disp_enhanced_image()

    def _print_score(self):
        print('--- score ---')
        for scored_param in self.scored_param_list:
            print('- %i' % (scored_param['score']))
        print('--- +++ ---')

    def _print_index_list(self):
        print('--- index list ---')
        print('- current: %s' % (self.current_image_parameter_index_list))
        print('- next: %s' % (self.next_image_parameter_index_list))
        print('--- +++ ---')

    def _write_scored_parameter_to_csv(self):
        save_list = [scored_param['param']
                     for scored_param in self.scored_param_list]
        for i in range(len(save_list)):
            save_list[i]['score'] = self.scored_param_list[i]['score']

        field_name_list = save_list[0].keys()

        with filedialog.asksaveasfile(mode='w', defaultextension='.csv') as f:
            if f is None:
                return

            writer = csv.DictWriter(
                f, fieldnames=field_name_list, delimiter=",", quotechar='"')
            writer.writeheader()

            for save_item in save_list:
                writer.writerow(save_item)

        print('write csv')
