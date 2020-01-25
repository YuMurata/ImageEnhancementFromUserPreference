import tensorflow as tf
import numpy as np

from UserPreferencePredictor.Model import PredictModel, ShapeTuple, ImageList
import enum


class ModelType(enum.Enum):
    MOBILE = enum.auto()
    RES = enum.auto()
    NAS = enum.auto()


class NIMA(PredictModel):
    def __init__(self, image_shape: ShapeTuple, model_type: ModelType):
        super().__init__(image_shape)
        self.model = self._build(model_type)

    def _build(self, model_type: ModelType):
        model_dict = {
            ModelType.MOBILE: {
                'model': tf.keras.applications.MobileNet((None, None, 3), alpha=1,
                                                         include_top=False, pooling='avg', weights=None),
                'weights_path': r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\IEFUP\NIMA\weights\mobilenet_weights.h5'
            },
            ModelType.RES: {
                'model': tf.keras.applications.InceptionResNetV2(input_shape=(None, None, 3), include_top=False, pooling='avg', weights=None),
                'weights_path': r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\IEFUP\NIMA\weights\inception_resnet_weights.h5'
            },
            ModelType.NAS: {
                'model': tf.keras.applications.NASNetMobile(input_shape=(224, 224, 3), include_top=False, pooling='avg', weights=None),
                'weights_path': r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\IEFUP\NIMA\weights\nasnet_weights.h5'
            },
        }

        base_model = model_dict[model_type]['model']
        x = tf.keras.layers.Dropout(0.75)(base_model.output)
        x = tf.keras.layers.Dense(10, activation='softmax')(x)

        weights_file_path = model_dict[model_type]['weights_path']
        model = tf.keras.Model(base_model.input, x)
        model.load_weights(weights_file_path)
        return model

    def predict(self, data_list: ImageList) -> np.array:
        image_array_list = np.array([self._image_to_array(data)
                                     for data in data_list])

        scores_list = self.model.predict(image_array_list)

        return np.array([self._mean_score(scores) for scores in scores_list])

    def _mean_score(self, scores):
        si = np.arange(1, 11, 1)
        mean = np.sum(scores * si)
        return [mean]
