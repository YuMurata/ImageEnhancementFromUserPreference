import matplotlib.pyplot as plt
from IEFUP.ImageEnhancer import ImageEnhancer
import config
import numpy as np


if __name__ == "__main__":
    enhancer = ImageEnhancer(r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\katsudon\1\1.jpg')

    fig, ax=plt.subplots()
    ax.imshow(np.array(enhancer.enhance(config.target_param_dict)))
    ax.set_axis_off()
    plt.show()
