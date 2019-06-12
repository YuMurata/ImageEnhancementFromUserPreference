import csv
from tkinter.filedialog import askopenfiles


def get_scored_param_list():
    scored_param_file_list = \
        askopenfiles(
            'r', title='スコアリングされたパラメータデータを選択してください',
            filetypes=[('scored param file', ['.csv'])])

    if not scored_param_file_list:
        raise FileNotFoundError('ファイルが選択されませんでした')

    return _format_scored_param_file_list(scored_param_file_list)


def _format_scored_param_file_list(scored_param_file_list: list):
    scored_param_list = []
    for param_file in scored_param_file_list:
        scored_param_list.extend(_read_scored_param(param_file))

    return scored_param_list


def _read_scored_param(param_file) -> list:
    read_dict = csv.DictReader(param_file, delimiter=",", quotechar='"')

    scored_param_list = [dict(zip(row.keys(), map(float, row.values())))
                         for row in read_dict]

    return scored_param_list


if __name__ == "__main__":
    print(get_scored_param_list())
