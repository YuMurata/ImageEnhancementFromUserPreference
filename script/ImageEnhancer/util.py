from tkinter.filedialog import askopenfilename
from ImageEnhancer.image_enhancer import ImageEnhancer


def get_image_path():
    image_path = \
        askopenfilename(
            title='画像を選択してください',
            filetypes=[('image file', ['.png', '.jpg'])])

    if not image_path:
        raise FileNotFoundError('ファイルが選択されませんでした')

    return image_path


def get_image_enhancer():
    try:
        image_path = get_image_path()
    except FileNotFoundError:
        print('画像ファイルが選択されなかったため終了します')
        exit()

    return ImageEnhancer(image_path)
