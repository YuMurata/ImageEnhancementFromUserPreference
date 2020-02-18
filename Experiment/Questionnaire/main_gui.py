import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
import IEFUP.ImageEnhancer as IE
from PreferenceOptimizer import ParameterOptimizer
from make_train_data import make_train_data, MakeTrainDataException
from threading import Thread, Event
from train_predictor import train, TrainPredictorException
from config.path import root_tfrecords_dir_path, root_summary_dir_path, root_image_dir_path, root_optimize_dir_path

from GUIParts import ProgressThread
from IEFUP.Optimize import EnhanceDecorder, EnhanceGenerator, EnhanceGeneratorException, CanvasGroupFrame
from config.dataset import IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_SHAPE
from misc import get_save_dir_path
from pathlib import Path
import itertools
from UserPreferencePredictor.Model import RankNet


class InputTextParts:
    def __init__(self, master, label: str):
        self.text_var = tk.StringVar(master)
        self.label = ttk.Label(master, text=label, padding=(5, 2))
        self.entry = ttk.Entry(master, textvariable=self.text_var)


class InputFrame(ttk.Frame):
    def __init__(self, master):
        super(InputFrame, self).__init__(master, padding=10)

        user_name_parts = InputTextParts(self, 'user name')
        image_name_parts = InputTextParts(self, 'image name')
        parts_list = [user_name_parts, image_name_parts]

        self.user_name_var = user_name_parts.text_var
        self.image_name_var = image_name_parts.text_var

        for index, parts in enumerate(parts_list):
            parts.label.grid(row=index, column=0, sticky=tk.E)
            parts.entry.grid(row=index, column=1)

    def get_user_name(self):
        return self.user_name_var.get()

    def get_image_name(self):
        return self.image_name_var.get()


class TrainThread(Thread):
    def __init__(self, user_name: str, image_name: str, tfrecords_dir_path: str, complete_event: Event):
        super(TrainThread, self).__init__()

        self.user_name = user_name
        self.image_name = image_name
        self.tfrecords_dir_path = tfrecords_dir_path
        self.complete_event = complete_event

    def run(self):
        try:
            train(self.user_name, self.image_name,
                  self.tfrecords_dir_path, epochs=20)
        except TrainPredictorException as e:
            tk.messagebox.showerror('error', e)
        finally:
            self.complete_event.set()


class OptimizeThread(Thread):
    def __init__(self, weights_file_path: str, image_file_path: Path, user_name: str, image_name: str, complete_event: Event):
        super(OptimizeThread, self).__init__()

        self.rank_net = RankNet(IMAGE_SHAPE, use_vgg16=False)
        self.rank_net.trainable_model.load_weights(weights_file_path)

        self.enhancer = IE.ImageEnhancer(
            str(image_file_path), (IMAGE_WIDTH, IMAGE_HEIGHT))
        enhance_generator = EnhanceGenerator(self.enhancer)
        self.optimizer = ParameterOptimizer(
            self.rank_net, enhance_generator, EnhanceDecorder())

        self.image_file_path = image_file_path
        self.user_name, self.image_name = user_name, image_name

        self.complete_event = complete_event

    def run(self):
        best_param_list, _ = self.optimizer.optimize(10)
        self.complete_event.set()

        sub_win = tk.Toplevel(root)

        def save_dir_path_func():
            image_number = self.image_file_path.parent.name
            return get_save_dir_path(
                root_optimize_dir_path, self.user_name, f'{self.image_name}/{image_number}')

        CanvasGroupFrame(sub_win, best_param_list,
                         self.enhancer, save_dir_path_func).pack()


if __name__ == "__main__":
    root = tk.Tk()
    input_frame = InputFrame(root)
    input_frame.pack()

    process_frame = ttk.Frame(root, padding=10)

    def make_train_data_command():
        try:
            make_train_data(root, input_frame.get_user_name(),
                            input_frame.get_image_name())
        except MakeTrainDataException as e:
            tk.messagebox.showerror('error', e)

    def train_predictor_command():
        user_name, image_name = input_frame.get_user_name(), input_frame.get_image_name()
        init_dir = root_tfrecords_dir_path/user_name/image_name

        tfrecords_dir_path = tk.filedialog.askdirectory(
            initialdir=init_dir, title='select tfrecords dir')

        progress_thread = ProgressThread(root, 'train now')
        train_thread = TrainThread(
            user_name, image_name, tfrecords_dir_path, progress_thread.complete_event)

        train_thread.start()
        progress_thread.start()

    def optimize_command():
        user_name, image_name = input_frame.get_user_name(), input_frame.get_image_name()

        weights_init_dir = root_summary_dir_path/user_name/image_name
        weights_file_path = tk.filedialog.askopenfilename(
            initialdir=weights_init_dir, title='select weights file', filetypes=[('', '*.h5')])
        if not weights_file_path:
            tk.messagebox.showerror('error', 'select weights file')
            return

        image_init_dir = root_image_dir_path/image_name
        image_dir_path = tk.filedialog.askdirectory(
            initialdir=image_init_dir, title='select optimize image dir')

        if not image_dir_path:
            tk.messagebox.showerror('error', 'select image file')
            return

        image_dir_path = Path(image_dir_path)
        image_file_path_list = list(itertools.chain(
            image_dir_path.glob('*.png'), image_dir_path.glob('*.jpg')))
        if len(image_file_path_list) != 1:
            tk.messagebox.showerror(
                'error', 'too many image files in directory')
            return

        image_file_path = image_file_path_list[0]

        try:
            progress_thread = ProgressThread(root, 'optimize now')
            optimize_thread = OptimizeThread(
                weights_file_path, image_file_path, user_name, image_name, progress_thread.complete_event)

            optimize_thread.start()
            progress_thread.start()

        except (EnhanceGeneratorException, IE.ImageEnhancerException) as e:
            tk.messagebox.showerror('error', e)

    ttk.Button(process_frame, text='make train data',
               padding=5, command=make_train_data_command).pack(side=tk.LEFT)
    ttk.Button(process_frame, text='train predictor',
               padding=5, command=train_predictor_command).pack(side=tk.LEFT)
    ttk.Button(process_frame, text='optimize',
               command=optimize_command, padding=5).pack(side=tk.LEFT)

    process_frame.pack()

    root.mainloop()
