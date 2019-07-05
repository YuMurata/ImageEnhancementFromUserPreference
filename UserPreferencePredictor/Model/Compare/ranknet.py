import tensorflow as tf
from UserPreferencePredictor.Model.Compare.dataset \
    import IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNEL
from evaluate_network import EvaluateNetwork
from pathlib import Path
import numpy as np

layers = tf.keras.layers
losses = tf.keras.losses


class RankNet:
    SCOPE = 'predict_model'
    PREDICTABLE_MODEL_FILE_NAME = 'predictable_model.h5'
    TRAINABLE_MODEL_FILE_NAME = 'trainable_model.h5'

    def __init__(self):
        with tf.name_scope(RankNet.SCOPE):
            evaluate_network = EvaluateNetwork()

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
              valid_dataset: tf.data.Dataset):
        callbacks = tf.keras.callbacks

        cb = []

        cb.append(callbacks.EarlyStopping())

        if log_dir_path is not None:
            cb.append(callbacks.TensorBoard(log_dir=log_dir_path,
                                            histogram_freq=1,
                                            write_graph=True,
                                            write_images=True))

        self.trainable_model.fit(dataset, epochs=10, steps_per_epoch=30,
                                 callbacks=cb, validation_data=valid_dataset,
                                 validation_steps=10)

    def save(self, save_dir_path: str):
        self.predictable_model.save(
            str(Path(save_dir_path)/RankNet.PREDICTABLE_MODEL_FILE_NAME),
            include_optimizer=False)

        self.trainable_model.save(
            Path(save_dir_path)/RankNet.TRAINABLE_MODEL_FILE_NAME)

    def load(self, load_dir_path: str):
        self.predictable_model.load(
            str(Path(load_dir_path)/RankNet.PREDICTABLE_MODEL_FILE_NAME),
            compile=False)

        self.trainable_model.load(
            Path(load_dir_path)/RankNet.TRAINABLE_MODEL_FILE_NAME)

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

    def predict(self, image_array: np.array):
        return self.predictable_model.predict(image_array)


if __name__ == '__main__':
    from UserPreferencePredictor.Model.Compare.dataset import make_dataset

    image_shape = (IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNEL)

    data_length = 100
    data_shape = (data_length, )+image_shape

    val_length = 50
    val_shape = (val_length, )+image_shape

    like_data = np.random.normal(0.2, 0.03, data_shape)
    unlike_data = np.random.normal(0.8, 0.03, data_shape)
    label = np.zeros(data_length)

    val_like_data = np.random.normal(0.2, 0.03, val_shape)
    val_unlike_data = np.random.normal(0.8, 0.03, val_shape)
    val_label = np.zeros(val_length)

    # dataset = tf.data.Dataset.from_tensor_slices(
    #     ((like_data, unlike_data), label)).batch(32).repeat()

    # valid_dataset = tf.data.Dataset.from_tensor_slices(
    #     ((val_like_data, val_unlike_data), val_label)).batch(32).repeat()

    model = RankNet()

    log_dir_path = Path(__file__).parent/'log'
    dataset_dir_path = Path(__file__).parent/'tfrecords'

    train_dataset_path = str(dataset_dir_path/'train.tfrecords')
    train_dataset = make_dataset(train_dataset_path, 32, 'train')

    valid_dataset_path = str(dataset_dir_path/'validation.tfrecords')
    valid_dataset = make_dataset(valid_dataset_path, 32, 'test')

    model.train(train_dataset, log_dir_path=str(log_dir_path),
                valid_dataset=valid_dataset)

    good = model.predict(np.random.normal(0.2, 0.03, (1,)+image_shape))
    bad = model.predict(np.random.normal(0.8, 0.03, (1,)+image_shape))

    print(f'good: {good}')
    print(f'bad: {bad}')
