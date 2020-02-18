from pathlib import Path
from IEFUP.ImageEnhancer import ImageEnhancer
import json


if __name__ == "__main__":
    target_dir = Path(__file__).parent / 'target'
    scored_param_dir = target_dir / 'scored_param'
    trainable_dir = target_dir / 'trainable'

    for user_score_dir in scored_param_dir.iterdir():
        user_name = user_score_dir.name
        enhance_dir = target_dir / 'enhance' / user_name
        enhance_dir.mkdir(exist_ok=True, parents=True)

        for image_path in trainable_dir.iterdir():
            category_name = image_path.stem

            param_path = scored_param_dir / user_name / f'{category_name}.json'
            if not param_path.exists():
                continue

            with open(str(param_path), 'r') as fp:
                best_param = sorted(
                    json.load(fp), key=lambda x: x['score'])[-1]['param']

            enhancer = ImageEnhancer(str(image_path))
            enhancer.enhance(best_param).save(
                str(enhance_dir / f'{category_name}.png'))
