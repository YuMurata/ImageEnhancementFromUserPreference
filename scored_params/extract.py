from pathlib import Path
import shutil

if __name__ == "__main__":
    root_dir = Path(__file__).parent

    for user_dir in root_dir.iterdir():
        if not user_dir.is_dir():
            continue

        for category_dir in user_dir.iterdir():
            if not category_dir.is_dir():
                continue

            file_path = str(category_dir/'scored_param.json')
            move_path = str(user_dir/f'{category_dir.name}.json')

            try:
                shutil.move(file_path, move_path)
            except FileNotFoundError as e:
                print(e)

            category_dir.rmdir()
