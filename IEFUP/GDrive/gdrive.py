from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from pathlib import Path

root_dir = 'UserPreferencePredictor'


def get_drive():
    os.chdir(str(Path(__file__).parent))

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    return GoogleDrive(gauth)


def upload(upload_file_path: str, dest_dir_path: str, *, upload_file_name: str = None):
    if not Path(upload_file_path).exists():
        raise FileNotFoundError

    drive = get_drive()

    dir_id = 'root'
    for dir_name in dest_dir_path.split('/'):
        dir_list = drive.ListFile(
            {'q': f'title = "{dir_name}" and "{dir_id}" in parents'}).GetList()

        if len(dir_list) == 0:
            drive.CreateFile({'title': f'{dir_name}',
                              'mimeType': 'application/vnd.google-apps.folder',
                              'parents': [{'id': dir_id}]}).Upload()
            dir_list = drive.ListFile(
                {'q': f'title = "{dir_name}" and "{dir_id}" in parents'}).GetList()
        dir_id = dir_list[0]['id']

    drive_file = drive.CreateFile({'parents': [{'id': dir_id}]})

    drive_file.SetContentFile(upload_file_path)
    drive_file['title'] = Path(
        upload_file_path).name if upload_file_name is None else upload_file_name

    drive_file.Upload()
