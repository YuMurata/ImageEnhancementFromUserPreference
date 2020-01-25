from pathlib import Path
from IEFUP.submodule import RankNet

IMAGE_SHAPE = (224, 224, 3)


if __name__ == "__main__":
    save_dir = Path(__file__).parent/'structure'
    save_dir.mkdir(exist_ok=True, parents=True)
    RankNet(IMAGE_SHAPE).structure.save(str(save_dir), show_layer_names=True, expand_nested=False)
