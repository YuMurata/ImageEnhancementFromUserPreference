from .image import image_name_list
from pathlib import Path

summary_dir_path = Path(
    r'C:\Users\init\Documents\PythonScripts\EnhanceImageFromUserPreference\Experiment\PerformanceEvaluation\Estimator\TrainData')/'summary'
summary_dir_path.mkdir(parents=True, exist_ok=True)

summary_dir_path_dict = {image_name: str(summary_dir_path/image_name)
                         for image_name in image_name_list}
