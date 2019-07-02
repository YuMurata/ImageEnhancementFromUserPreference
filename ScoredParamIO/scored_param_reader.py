import csv
from tkinter.filedialog import askopenfilenames


def get_scored_param_list():
    scored_param_file_path_list = \
        askopenfilenames(
            title='スコアリングされたパラメータデータを選択してください',
            filetypes=[('scored param file', ['.csv'])])

    if not scored_param_file_path_list:
        raise FileNotFoundError('ファイルが選択されませんでした')

    return format_scored_param_file_list(scored_param_file_path_list)


def format_scored_param_file_list(scored_param_file_path_list: list):
    scored_param_list = []
    for param_file_path in scored_param_file_path_list:
        scored_param_list.extend(read_scored_param(param_file_path))

    return scored_param_list


def read_scored_param(param_file_path: str) -> list:
    with open(param_file_path) as param_file:
        read_dict = csv.DictReader(param_file, delimiter=",", quotechar='"')
        scored_param_list = \
            [dict(zip(row.keys(), map(float, row.values())))
             for row in read_dict]

    return scored_param_list


if __name__ == "__main__":
    print(get_scored_param_list())
