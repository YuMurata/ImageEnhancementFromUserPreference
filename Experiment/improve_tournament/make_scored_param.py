from IEFUP.TrainDataMaker.make_cut_out import tournament
from IEFUP.ImageEnhancer import enhance_name_list
import json
from pathlib import Path
from IEFUP.GDrive import upload

if __name__ == "__main__":
    scored_player_list = tournament(
        100, dict(zip(enhance_name_list, [1.2, 1.2, 1.2, 1.2])))

    save_dir_path = Path(
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\improve_tournament\scored_param')
    image_name = 'salad'
    save_file_path = str(save_dir_path/(image_name+'.json'))

    scored_dict_list = [{'score': player.score, 'param': player.param}
                        for player in scored_player_list]
    save_dict = {'image_name': image_name, 'scored_params': scored_dict_list}

    with open(save_file_path, 'w') as fp:
        json.dump(save_dict, fp, indent=4)

    upload(save_file_path, 'scored_param')
