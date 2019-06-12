from GUI.comparer import CompareCanvasGroupFrame

from tkinter import simpledialog, Tk
from ImageEnhancer.util import get_image_enhancer

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()

    image_enhancer = get_image_enhancer()

    generate_num = \
        simpledialog.askinteger('value', 'データ生成数を入力してください（2以上）',
                                minvalue=2, initialvalue=2)
    if not generate_num:
        exit()

    root.deiconify()

    canvas = CompareCanvasGroupFrame(root)
    canvas.pack()

    canvas.make_image_generator(image_enhancer, generate_num)
    canvas.disp_enhanced_image()

    root.mainloop()
