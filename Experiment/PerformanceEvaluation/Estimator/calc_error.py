from config.result import result_dir_path_dict, param_type_list
from PIL import Image
from SSIM_PIL import compare_ssim
from pathlib import Path
import json


if __name__ == "__main__":
    for image_name, result_dir_path in result_dir_path_dict.items():
        result_dir_path = Path(result_dir_path)

        image_dict = {key: Image.open(str(result_dir_path/(key+'.png'))) for key in param_type_list}

        data_dict = {}

        with open(str(result_dir_path/'data.json')) as fp:
            data_dict = json.load(fp)

        if 'optimize-target_error' not in data_dict:
            continue

        target_error = data_dict.pop('optimize-target_error')
        train_error = data_dict.pop('optimize-train_error')

        param_error_dict = {
            'optimize-target': target_error,
            'optimize-train': train_error
        }

        ssim_error_dict = {
            'optimize-target': compare_ssim(image_dict['optimize'], image_dict['target']),
            'optimize-train': compare_ssim(image_dict['optimize'], image_dict['train_dataset'])
        }

        data_dict['error'] = {
                'param': param_error_dict,
                'ssim': ssim_error_dict
            }

        with open(str(result_dir_path/'data.json'), 'w') as fp:
            json.dump(data_dict, fp, indent=4)



