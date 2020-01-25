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

katsudon_path_list = [
    r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\katsudon\1\1.jpg',
    r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\katsudon\2\2.png']

salad_path_list = [
    r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\salad\1\1.jpg',
    r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\salad\2\2.jpg',
    r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\salad\3\3.jpg']


image_path_dict = {
    'katsudon': katsudon_path_list,
    'salad': salad_path_list
}

IMAGE_SHAPE = IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNEL = 224, 224, 3
IMAGE_SIZE = IMAGE_WIDTH, IMAGE_HEIGHT
