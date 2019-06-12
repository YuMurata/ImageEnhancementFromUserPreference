import csv
import tkinter
from tkinter import filedialog

import matplotlib.pyplot as plt
import numpy as np
from gauss import make_gauss_graph_variable
from mpl_toolkits.mplot3d import Axes3D


def scatter_graph(param_file_list: list, figure: plt.Figure):
    for param_index, param_file in enumerate(param_file_list):
        read_dict = csv.DictReader(param_file, delimiter=",", quotechar='"')
        key_list = read_dict.fieldnames

        dict_list = [dict(zip(row.keys(), map(float, row.values())))
                     for row in read_dict]
        score_list = [item['score'] for item in dict_list]

        for key in key_list:
            if key == 'score':
                continue

            item_list = [item[key] for item in dict_list]

            if key not in ax_dict:
                ax_dict[key] = figure.add_subplot(2, 2, key_list.index(key)+1)
                ax_dict[key].set_title(key)

            ax_dict[key].scatter(
                np.array(item_list), np.array(score_list),
                c=color_list[param_index], label='実験%i' % (param_index+1))

    plt.show()


def gauss_graph(param_file_list: list, figure: plt.Figure):
    for param_index, param_file in enumerate(param_file_list):
        read_dict = csv.DictReader(param_file, delimiter=",", quotechar='"')
        key_list = read_dict.fieldnames
        assert len(key_list) == 3

        dict_list = [dict(zip(row.keys(), map(float, row.values())))
                     for row in read_dict]

        X, Y, Z, label_list = make_gauss_graph_variable(dict_list)

        ax = figure.add_subplot(1, 1, param_index+1, projection='3d')
        ax.set_xlabel(label_list[0], size=16)
        ax.set_ylabel(label_list[1], size=16)
        ax.set_zlabel(label_list[2], size=16)
        ax.plot_surface(X, Y, Z, cmap='coolwarm', cstride=1, rstride=1)

    plt.show()


if __name__ == "__main__":
    root = tkinter.Tk()
    root.attributes('-topmost', True)

    root.withdraw()
    root.lift()
    root.focus_force()

    param_file_list = \
        filedialog.askopenfiles(
            'r', title='select scored_param data as csv',
            filetypes=[('scored param', ['.csv'])])
    root.destroy()

    if not param_file_list:
        exit()

    scored_param_list_dict = {}

    figure = plt.figure(figsize=(8, 8))
    ax_dict = {}
    color_list = ['red', 'blue', 'green', 'yellow']

    #gauss_graph(param_file_list, figure)
    scatter_graph(param_file_list, figure)
