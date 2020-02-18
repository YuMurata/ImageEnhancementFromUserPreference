from UserPreferencePredictor.TrainDataMaker import Player
from IEFUP.ImageEnhancer import ImageEnhancer, Image


class EnhancedPlayer(Player):
    def __init__(self, param: dict, enhancer: ImageEnhancer):
        super().__init__(param)
        self.enhancer = enhancer

    def decode(self) -> Image:
        return self.enhancer.enhance(self.param)
