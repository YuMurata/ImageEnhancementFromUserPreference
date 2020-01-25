from IEFUP.ImageEnhancer import enhance_name_list

target_param_dict = {
    'katsudon': {
        'path': r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\katsudon\1\1.jpg',
        'param': dict(zip(enhance_name_list, [1.2, 1.2, 1.2, 1.2])),
    },
    'salad': {
        'path': r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\salad\1\1.jpg',
        'param': dict(zip(enhance_name_list, [1.2, 1.2, 1.2, 1.2])),
    }
}

IMAGE_SHAPE = IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNEL = 224, 224, 3
IMAGE_SIZE = IMAGE_WIDTH, IMAGE_HEIGHT
