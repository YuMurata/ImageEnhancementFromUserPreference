from datetime import datetime
from pathlib import Path


class MiscException(Exception):
    pass


def get_save_dir_path(root_dir_path: Path, user_name: str, image_name: str) -> str:
    if not user_name:
        raise MiscException('invalid user name')
    if not image_name:
        raise MiscException('invalid image name')

    now = datetime.now()
    date = '{0:%m%d}'.format(now)
    time = '{0:%H%M}'.format(now)

    dir_path = root_dir_path / \
        user_name/image_name/date/time

    dir_path.mkdir(exist_ok=True, parents=True)
    return str(dir_path)


def get_save_file_path(save_dir_path: str, save_file_name: str) -> str:
    save_dir_path = Path(save_dir_path)
    save_dir_path.mkdir(exist_ok=True, parents=True)

    return str(save_dir_path/save_file_name)
