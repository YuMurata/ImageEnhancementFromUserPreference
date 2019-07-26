from ParameterOptimizer.main import optimize
from config.train import summary_dir_path_dict
from pathlib import Path
from ImageEnhancer.image_enhancer import ImageEnhancer
from config.image import image_path_dict
from config.result import result_dir_path_dict, param_type_list
from config.param import param_path_dict
import json
from ScoredParamIO.scored_param_reader import read_scored_param
from ImageEnhancer.enhance_definer import enhance_name_list
import math
from SSIM_PIL import compare_ssim


def find_best_train_param():
    param_file_path = param_path_dict['train']
    scored_param_list = read_scored_param(param_file_path)
    best_param = max(scored_param_list, key=lambda x: x['score'])

    return best_param


def optimize_images(enhancer_dict: dict):
    optimized_param_dict = {}
    for image_name, summary_dir_path in summary_dir_path_dict.items():
        summary_dir_path = Path(summary_dir_path)
        load_dir_path = str(
            list(list(summary_dir_path.iterdir())[-1].iterdir())[-1])

        enhancer = enhancer_dict[image_name]

        optimized_param_dict[image_name] = optimize(
            load_dir_path, 'compare', enhancer)[0]

    return optimized_param_dict


def calc_error(x_dict: dict, y_dict: dict):
    assert all([x_key == y_key for x_key, y_key in zip(
        x_dict.keys(), y_dict.keys())])
    squared_diff_list = [(x_dict[key]-y_dict[key])**2 for key in x_dict.keys()]
    RMSE = math.sqrt(sum(squared_diff_list)/len(squared_diff_list))
    return RMSE


if __name__ == "__main__":
    enhancer_dict = {image_name: ImageEnhancer(image_path)
                     for image_name, image_path in image_path_dict.items()}

    optimized_param_dict = optimize_images(enhancer_dict)
    best_train_param = find_best_train_param()
    target_param = {enhance_name: 1 for enhance_name in enhance_name_list}

    for image_name, optimized_param in optimized_param_dict.items():
        result_dir_path = Path(result_dir_path_dict[image_name])
        result_dir_path.mkdir(parents=True, exist_ok=True)

        param_dict = {
            'optimize': optimized_param,
            'target': target_param,
            'train_dataset': best_train_param
        }

        enhancer = enhancer_dict[image_name]
        image_dict = {}
        for param_type in param_type_list:
            image_dict[param_type] = enhancer.org_enhance(
                param_dict[param_type])
            image_dict[param_type].save(
                str(result_dir_path/(param_type+'.png')))

        param_error_dict = {
            'optimize-target': calc_error(optimized_param, target_param),
            'optimize-train': calc_error(optimized_param, best_train_param),
        }

        ssim_error_dict = {
            'optimize-target': compare_ssim(image_dict['optimize'], image_dict['target']),
            'optimize-train': compare_ssim(image_dict['optimize'], image_dict['train_dataset'])
        }
        write_data = {
            'param': param_dict,
            'error': {
                'param': param_error_dict,
                'ssim': ssim_error_dict
            }
        }

        with open(str(result_dir_path/'data.json'), 'w') as fp:
            json.dump(write_data, fp, indent=4)
