import matplotlib.pyplot as plt
from IEFUP.ImageEnhancer import ImageEnhancer
import config
import numpy as np


if __name__ == "__main__":
    fig = plt.figure()
    for i, (image_name, value) in enumerate(config.target_param_dict.items(), start=1):
        enhancer = ImageEnhancer(value['path'])
        ax = fig.add_subplot(1, 2, i)
        ax.imshow(np.array(enhancer.enhance(value['param'])))

        ax.set_title(image_name)
        ax.set_axis_off()

    plt.show()
