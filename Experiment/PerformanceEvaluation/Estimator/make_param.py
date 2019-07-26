from Quantifier.identify.param_maker import main
from config.param import param_path_dict, generate_num_dict

if __name__ == "__main__":
    for datatype, save_file_path in param_path_dict.items():
        main(generate_num=generate_num_dict[datatype],
             save_file_path=save_file_path,
             target_param=1)
