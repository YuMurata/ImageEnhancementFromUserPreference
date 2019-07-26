from .image import image_name_list
from pathlib import Path

result_root_dir_path = Path(
    r'C:\Users\init\Documents\PythonScripts\EnhanceImageFromUserPreference\Experiment\PerformanceEvaluation\Estimator\Result')

result_dir_path_dict = {image_name: str(result_root_dir_path/image_name)
                        for image_name in image_name_list}
