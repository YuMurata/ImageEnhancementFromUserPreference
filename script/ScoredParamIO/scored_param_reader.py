import csv


def read_scored_param(param_file_path: str) -> list:
    with open(param_file_path) as param_file:
        read_dict = csv.DictReader(param_file, delimiter=",", quotechar='"')
        scored_param_list = \
            [dict(zip(row.keys(), map(float, row.values())))
             for row in read_dict]

    return scored_param_list


