from PIL.ImageEnhance import Brightness, Color, Contrast, Sharpness


enhance_dict = {
    'brightness': Brightness,
    'saturation': Color,
    'contrast':  Contrast,
    'sharpness': Sharpness
}

enhance_class_list = enhance_dict.values()
enhance_name_list = enhance_dict.keys()
