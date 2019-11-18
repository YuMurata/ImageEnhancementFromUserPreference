import tkinter as tk
from tkinter import ttk
from make_train_data import make_train_data, MakeTrainDataException
from train_predictor import train, TrainPredictorException
from optimize import optimize
from config.path import root_tfrecords_dir_path
from threading import Thread


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
            print(e)

    def train_predictor_command():
        try:
            user_name, image_name = input_frame.get_user_name(), input_frame.get_image_name()
            init_dir = root_tfrecords_dir_path/user_name/image_name

            tfrecords_dir_path = tk.filedialog.askdirectory(
                initialdir=init_dir, title='select tfrecords dir')

            sub_win = tk.Toplevel(root)
            ttk.Label(sub_win, text='train now').pack()
            progress = ttk.Progressbar(sub_win)
            progress.configure(value=0, mode='indeterminate', maximum=100)
            progress.pack()
            progress.start(interval=10)

            sub_win.grab_set()
            sub_win.protocol('WM_DELETE_WINDOW', lambda: pass)

            thread = Thread(target=lambda: train(
                user_name, image_name, tfrecords_dir_path))
            import time
            thread = Thread(target=lambda: time.sleep(5))
            thread.start()
            thread.join()

            sub_win.wait_window()
            print('aho')
            sub_win.destroy()

        except TrainPredictorException as e:
            print(e)

    def optimize_command():
        try:
            optimize(root, input_frame.get_user_name(),
                     input_frame.get_image_name())
        except MakeTrainDataException as e:
            print(e)

    ttk.Button(process_frame, text='make train data',
               padding=5, command=make_train_data_command).pack(side=tk.LEFT)
    ttk.Button(process_frame, text='train predictor',
               padding=5, command=train_predictor_command).pack(side=tk.LEFT)
    ttk.Button(process_frame, text='optimize', padding=5).pack(side=tk.LEFT)
    process_frame.pack()

    root.mainloop()
