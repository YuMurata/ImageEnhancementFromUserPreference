from IEFUP.Optimize \
    import EnhanceGenerator, EnhanceDecorder, Predictor, ParameterOptimizer
from pathlib import Path
import pickle

IMAGE_SHAPE = (224, 224, 3)
IMAGE_SIZE = (224, 224)

if __name__ == "__main__":

    optimize_dir_path = Path(__file__).parent / 'optimize'
    weights_dir_path = Path(__file__).parent / 'weights'
    optimizable_dir_path = Path(__file__).parent / 'optimizables'

    user_name_list = [
        'dobashi'
    ]

    for user_name in user_name_list:
        for category_dir_path in optimizable_dir_path.iterdir():
            category_name = category_dir_path.name
            weight_path = weights_dir_path / user_name / f'{category_name}.h5'

            if not weight_path.exists():
                print(f'{category_name}.h5 not found in {user_name}')
                continue

            for image_path in category_dir_path.iterdir():
                print(f'{user_name} - {image_path.name} in {category_name}')

                generator = EnhanceGenerator(str(image_path), IMAGE_SIZE)
                enhance_decoder = EnhanceDecorder()

                predictor = Predictor(str(weight_path))

                optimizer = \
                    ParameterOptimizer.Optimizer(predictor, generator,
                                                 enhance_decoder)
                best_param_list, logbook = \
                    optimizer.optimize(ngen=20, param_list_num=1)

                save_dir_path = optimize_dir_path / user_name / category_name
                save_dir_path.mkdir(parents=True, exist_ok=True)

                image_name = image_path.stem
                save_path = str(save_dir_path / f'{image_name}.png')
                generator.enhancer.enhance(best_param_list[0]).save(save_path)

                log_dir_path = save_dir_path / 'logs'
                log_dir_path.mkdir(exist_ok=True)
                log_path = str(log_dir_path / f'{image_name}.pkl')
                with open(log_path, 'wb') as fp:
                    pickle.dump(logbook, fp)
