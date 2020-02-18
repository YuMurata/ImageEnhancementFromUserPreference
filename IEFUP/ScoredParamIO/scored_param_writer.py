import csv


def write_scored_param(scored_param_dict_list: list, save_file_path: str):
    save_list = \
        [scored_param['param'] for scored_param in scored_param_dict_list]
    for i in range(len(save_list)):
        save_list[i]['score'] = scored_param_dict_list[i]['score']

    field_name_list = save_list[0].keys()

    with open(save_file_path, 'w') as file_obj:
        writer = csv.DictWriter(
            file_obj, fieldnames=field_name_list, delimiter=",", quotechar='"')
        writer.writeheader()

        for save_item in save_list:
            writer.writerow(save_item)


if __name__ == "__main__":
    write_scored_param([{'param': {'a': 1}, 'score': 1}])
