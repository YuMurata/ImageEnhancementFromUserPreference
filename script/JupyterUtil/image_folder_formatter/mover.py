import shutil
from pathlib import Path


def move_folder(dl_path: str):
    dl_path = Path(dl_path)

    image_path_list = \
        [path for path in dl_path.iterdir() if path.is_file()]
    folder_path_list = \
        [path for path in dl_path.iterdir() if path.is_dir()]

    for folder_path, image_path in zip(folder_path_list, image_path_list):
        shutil.move(str(image_path), str(folder_path)+'/')
