from UserPreferencePredictor.Model import RankNet
from PIL import Image
from pathlib import Path
import config
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    weights_dir_path = Path(
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\improve_tournament\weights')

    cam_dir_path = Path(r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\improve_tournament\grad_cam')

    cnn = RankNet(config.IMAGE_SHAPE, use_vgg16=False)
    vgg = RankNet(config.IMAGE_SHAPE, use_vgg16=True)

    records_num = 4000
    cnn_weights_path = str(weights_dir_path/'cnn'/f'{records_num}.h5')
    vgg_weights_path = str(weights_dir_path/'vgg'/f'{records_num}.h5')

    cnn.trainable_model.load_weights(cnn_weights_path)
    vgg.trainable_model.load_weights(vgg_weights_path)

    katsudon_path_list = [
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\katsudon\1\1.jpg',
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\katsudon\2\2.png']

    salad_path_list = [
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\salad\1\1.jpg',
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\salad\2\2.jpg',
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\salad\3\3.jpg']

    path_dict = {'katsudon': katsudon_path_list, 'salad': salad_path_list}
    key = 'salad'

    image_path = path_dict[key][2]

    for key in ['katsudon', 'salad']:
        for index, image_path in enumerate(path_dict[key]):
            image = Image.open(image_path).convert('RGB')

            cnn_cam = cnn.grad_cam.get_cam(np.array(image), 'conv2d_1')
            vgg_cam = vgg.grad_cam.get_cam(np.array(image), 'block5_conv3')

            save_dir_path = cam_dir_path/key/str(index)
            save_dir_path.mkdir(parents=True, exist_ok=True)
            Image.fromarray(cnn_cam).save(str(save_dir_path/'cnn.png'))
            Image.fromarray(vgg_cam).save(str(save_dir_path/'vgg.png'))
