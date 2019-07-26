from UserPreferencePredictor.predictor_trainer import main
from config.train import summary_dir_path_dict
from config.records import dataset_dir_path_dict
from config.image import image_name_list

if __name__ == "__main__":
    for image_name in image_name_list:
        main('compare', summary_dir_path_dict[image_name],
             None, dataset_dir_path_dict[image_name])
