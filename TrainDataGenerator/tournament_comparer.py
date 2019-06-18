from GUI.comparer import CompareCanvasGroupFrame

from tkinter import Tk
from ImageEnhancer.util import ImageEnhancer

from argparse import ArgumentParser


def _get_args():
    parser = ArgumentParser()
    parser.add_argument('-p', '--image_path', required=True)
    parser.add_argument('-n', '--generate_num', required=True, type=int)

    return parser.parse_args()


if __name__ == "__main__":
    args = _get_args()

    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    if args.generate_num < 2:
        raise ValueError('生成数は2以上にしてください')

    image_enhancer = ImageEnhancer(args.image_path)

    root = Tk()
    canvas = CompareCanvasGroupFrame(root)
    canvas.pack()

    canvas.make_image_generator(image_enhancer, args.generate_num)
    canvas.disp_enhanced_image()

    root.mainloop()
