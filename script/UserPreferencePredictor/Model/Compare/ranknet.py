import tensorflow as tf
from UserPreferencePredictor.Model.Compare.dataset \
    import IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNEL
from UserPreferencePredictor.Model.Compare.evaluate_network \
    import EvaluateNetwork
from pathlib import Path
import numpy as np
from PIL import Image
from UserPreferencePredictor.Model.Compare.grad_cam import GradCam

layers = tf.keras.layers
losses = tf.keras.losses

class RankNet:
    SCOPE = 'predict_model'
    PREDICTABLE_MODEL_FILE_NAME = 'predictable_model.h5'
    TRAINABLE_MODEL_FILE_NAME = 'trainable_model.h5'

    def __init__(self):
        with tf.name_scope(RankNet.SCOPE):
            # evaluate_network = EvaluateNetwork()
            self.grad_cam = GradCam(evaluate_network, (IMAGE_WIDTH, IMAGE_HEIGHT))

            input_shape = (IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNEL)

            left_input = tf.keras.Input(shape=input_shape)
            right_input = tf.keras.Input(shape=input_shape)

            left_output = evaluate_network(left_input)
            right_output = evaluate_network(right_input)

            concated_output = layers.Concatenate()([left_output, right_output])

            self.predictable_model = tf.keras.Model(inputs=left_input,
                                                    outputs=left_output)

            self.trainable_model = tf.keras.Model(inputs=[left_input,
                                                          right_input],
                                                  outputs=concated_output)

            loss = \
                tf.keras.losses.SparseCategoricalCrossentropy(
                    from_logits=True)
            self.trainable_model.compile(optimizer='adam', loss=loss)

    def train(self, dataset: tf.data.Dataset, *, log_dir_path: str,
              valid_dataset: tf.data.Dataset, epochs=10, steps_per_epoch=30):
        callbacks = tf.keras.callbacks

        cb = []

        # cb.append(callbacks.EarlyStopping())

        if log_dir_path is not None:
            cb.append(callbacks.TensorBoard(log_dir=log_dir_path,
                                            write_graph=True))

        self.trainable_model.fit(dataset, epochs=epochs,
                                 steps_per_epoch=steps_per_epoch,
                                 callbacks=cb, validation_data=valid_dataset,
                                 validation_steps=10)

    def save(self, save_dir_path: str):
        save_dir_path = Path(save_dir_path)
        if not save_dir_path.exists():
            save_dir_path.mkdir(parents=True)

        self.predictable_model.save_weights(
            str(Path(save_dir_path) /
                RankNet.PREDICTABLE_MODEL_FILE_NAME)
        )

        self.trainable_model.save_weights(
            str(Path(save_dir_path) /
                RankNet.TRAINABLE_MODEL_FILE_NAME))

    def load(self, load_dir_path: str):
        self.predictable_model.load_weights(
            str(Path(load_dir_path)/RankNet.PREDICTABLE_MODEL_FILE_NAME))

        self.trainable_model.load_weights(
            str(Path(load_dir_path)/RankNet.TRAINABLE_MODEL_FILE_NAME))

    def save_model_structure(self, save_dir_path: str):
        save_dir_path = Path(save_dir_path)
        if not save_dir_path.exists():
            save_dir_path.mkdir(parents=True)

        tf.keras.utils.plot_model(self.predictable_model,
                                  str(save_dir_path/'predictable_model.png'),
                                  show_shapes=True)

        tf.keras.utils.plot_model(self.trainable_model,
                                  str(save_dir_path/'trainable_model.png'),
                                  show_shapes=True)

    def _image_to_array(self, image: Image.Image):
        resized_image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        return np.asarray(resized_image).astype(np.float32)/255

    def predict(self, data_list: list):
        image_array_list = np.array([self._image_to_array(data['image'])
                                     for data in data_list])

        return self.predictable_model.predict(image_array_list)


if __name__ == '__main__':
    model = RankNet()
    model.load(r'C:\Users\init\Documents\PythonScripts\EnhanceImageFromUserPreference\Experiment\Questionnaire\summary\murata\katsudon\1102\1158')

    import matplotlib.pyplot as plt

    image_path_list = [
        r'C:\Users\init\Documents\PythonScripts\EnhanceImageFromUserPreference\Experiment\Questionnaire\image\katsudon\1\1.jpg',
        r'C:\Users\init\Documents\PythonScripts\EnhanceImageFromUserPreference\Experiment\Questionnaire\image\katsudon\2\2.png',
        r'C:\Users\init\Documents\PythonScripts\EnhanceImageFromUserPreference\Experiment\Questionnaire\image\salad\1\1.jpg',
        r'C:\Users\init\Documents\PythonScripts\EnhanceImageFromUserPreference\Experiment\Questionnaire\image\salad\2\2.jpg',
    ]

    for image_path in image_path_list:
        image = Image.open(image_path).convert('RGB')
        cam = model.grad_cam.get_cam(np.array(image))

        plt.figure()
        plt.imshow(cam)

    plt.show()