from IEFUP.Optimize \
    import EnhanceGenerator, EnhanceDecorder, Predictor, Optimizer
from pathlib import Path
import pickle

IMAGE_SHAPE = (224, 224, 3)
IMAGE_SIZE = (224, 224)

if __name__ == "__main__":

    optimize_dir_path = Path(__file__).parent/'optimize'
    weights_dir_path = Path(__file__).parent/'weights'
    optimizable_dir_path = Path(__file__).parent/'image'/'optimizable'

    weight_path_list = [
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Compare\weights\10-0.24-0.18_ejiri_katsudon.h5',
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Compare\weights\15-037-029_sakao_katsudon.h5',
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Compare\weights\18-0.37-0.38_ishikawa_katsudon.h5',
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Compare\weights\19-0.25-0.23_kawazumi_katsudon.h5',
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Compare\weights\19-030-028_oba_katsudon.h5',
    ]
    user_name_list = [
        'ejiri'
    ]

    for user_name in user_name_list:
        for category_dir_path in optimizable_dir_path.iterdir():
            category_name = category_dir_path.name
            weight_path = weights_dir_path/user_name/f'{category_name}.h5'

            if not weight_path.exists():
                raise FileNotFoundError(f'{category_name}.h5 not found in {user_name}')

            for image_path in category_dir_path.iterdir():

                generator = EnhanceGenerator(str(image_path), IMAGE_SIZE)
                enhance_decoder = EnhanceDecorder()

                predictor = Predictor(IMAGE_SHAPE, str(weight_path))

                best_param_list, logbook = Optimizer(
                    predictor, generator, enhance_decoder).optimize(ngen=20, param_list_num=1)

                save_dir_path = optimize_dir_path/user_name/category_name
                save_dir_path.mkdir(parents=True, exist_ok=True)

                image_name = image_path.stem
                save_path = str(save_dir_path/f'{image_name}.png')
                generator.enhancer.enhance(best_param_list[0]).save(save_path)

                log_dir_path = save_dir_path/'logs'
                log_dir_path.mkdir(exist_ok=True)
                log_path = str(log_dir_path/f'{image_name}.pkl')
                with open(log_path, 'wb') as fp:
                    pickle.dump(logbook, fp)
