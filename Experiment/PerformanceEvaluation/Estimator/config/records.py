from pathlib import Path
from .image import image_name_list

tfrecords_dir_path = Path(
    r'C:\Users\init\Documents\PythonScripts\EnhanceImageFromUserPreference\Experiment\PerformanceEvaluation\Estimator\TrainData\tfrecords')
dataset_dir_path_dict = {image_name: str(tfrecords_dir_path/image_name)
                         for image_name in image_name_list}
