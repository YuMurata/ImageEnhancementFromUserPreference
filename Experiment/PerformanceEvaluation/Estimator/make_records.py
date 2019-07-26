from TrainDataGenerator.TFRecordsMaker.ScoredParamConverter.conpare import main
from config.param import param_path_dict
from config.records import image_path_dict, save_dir_path_dict

if __name__ == "__main__":
    for image_name, image_path in image_path_dict.items():
        main(image_path, param_path_dict['train'], param_path_dict['validation'], save_dir_path_dict[image_name])
