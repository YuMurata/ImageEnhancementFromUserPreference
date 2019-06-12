from PIL import Image
from .enhance_definer import enhance_dict
from TrainDataGenerator.ScoredParamToTFRecordsConverter.util \
    import IMAGE_HEIGHT, IMAGE_WIDTH


class ImageEnhancer:
    def __init__(self, image_path: str):
        self.org_image = Image.open(image_path).convert('RGB')
        self.resize_image = self.org_image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))

    def _enhance(self, image_parameter: dict, image: Image.Image) \
            -> Image.Image:

        ret_image = image
        for enhance_name, enhance_class in enhance_dict.items():
            if enhance_name not in image_parameter:
                continue

            ret_image = enhance_class(ret_image).enhance(
                image_parameter[enhance_name])
        return ret_image

    def org_enhance(self, image_parameter: dict) -> Image.Image:
        return self._enhance(image_parameter, self.org_image)

    def resized_enhance(self, image_parameter: dict) -> Image.Image:
        return self._enhance(image_parameter, self.resize_image)


def plot_compare_image(left_image, right_image):
    import matplotlib.pyplot as plt
    import numpy as np

    figure = plt.figure()
    ax_list = [figure.add_subplot(1, 2, i+1) for i in range(2)]
    ax_list[0].imshow(np.asarray(left_image))
    ax_list[1].imshow(np.asarray(right_image))

    plt.show()


if __name__ == "__main__":
    import os
    print()
    ie = ImageEnhancer(os.path.join(os.path.dirname(__file__), 'img_16.jpg'))
    plot_compare_image(ie.enhance(
        {'brightness': 1.5}), ie.enhance({'brightness': 0.5}))
