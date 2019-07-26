from pathlib import Path

param_dir_path = Path(
    r'C:\Users\init\Documents\PythonScripts\EnhanceImageFromUserPreference\Experiment\PerformanceEvaluation\Estimator\TrainData\scored_param')

extension = '.csv'

datatype_list = ['train', 'validation']
generate_num_dict = {'train': 100, 'validation': 10}

param_path_dict = {
    datatype: str(param_dir_path / (datatype + extension)) for datatype in datatype_list}
