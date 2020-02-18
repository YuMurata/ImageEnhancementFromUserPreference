from IEFUP.submodule import ParameterOptimizer, ImageRankNet
from IEFUP.ImageRankNet.mycnn import MyCNN


class Predictor(ParameterOptimizer.PredictModel):
    def __init__(self, weight_path: str):
        self.model = ImageRankNet.RankNet(MyCNN())
        self.model.load(weight_path)

    def predict(self, image):
        return self.model.predict([image])[0][0]
