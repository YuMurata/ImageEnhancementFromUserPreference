from IEFUP.submodule import PredictModel, RankNet


class Predictor(PredictModel):
    def __init__(self, image_shape: tuple, weight_path: str):
        self.model = RankNet(image_shape)
        self.model.load(weight_path)

    def predict(self, image):
        return self.model.predict([image])[0][0]
