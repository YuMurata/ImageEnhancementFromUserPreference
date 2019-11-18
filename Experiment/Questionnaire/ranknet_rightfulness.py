from UserPreferencePredictor.Model.Compare.ranknet import RankNet
from argparse import ArgumentParser
import json
from PIL import Image, ImageDraw, ImageFont
from config.path import root_rightfulness_dir_path
from misc import get_save_dir_path, get_save_file_path
from tqdm import tqdm


def _get_args():
    parser = ArgumentParser()

    parser.add_argument('-l', '--load_dir_path', required=True)
    parser.add_argument('-s', '--scored_param_path', required=True)
    parser.add_argument('-u', '--user_name', required=True)
    parser.add_argument('-i', '--image_name', required=True)
    parser.add_argument('-n', '--image_number', required=True)

    args = parser.parse_args()
    for arg in vars(args):
        print(f'{str(arg)}: {str(getattr(args, arg))}')

    return args


if __name__ == "__main__":
    args = _get_args()

    predict_model = RankNet()

    try:
        predict_model.load(args.load_dir_path)
    except ValueError:
        print('ロードができなかったため終了します')
        exit()

    scored_param_list = None
    with open(args.scored_param_path, 'r') as fp:
        scored_param_list = json.load(fp)

    image_list = [{'image': Image.open(
        scored_param['param'])} for scored_param in scored_param_list]

    evaluate_list = predict_model.predict(image_list)

    for i in range(len(scored_param_list)):
        scored_param_list[i]['evaluate'] = evaluate_list[i][0]

    rightfulness_dir_path = get_save_dir_path(
        root_rightfulness_dir_path, args.user_name, f'{args.image_name}/{args.image_number}')

    scored_param_list.sort(key=lambda x: x['score'], reverse=True)

    for index, scored_param in enumerate(tqdm(scored_param_list)):
        image = Image.open(scored_param['param'])

        new_image = Image.new(
            image.mode, (image.width, image.height+100), (255, 255, 255))
        new_image.paste(image, (0, 0))

        draw = ImageDraw.Draw(new_image)

        text_dict = {key: f'{key:<10s}:{scored_param[key]:>5,.2f}' for key in [
            'score', 'evaluate']}

        font = ImageFont.truetype(r"C:\Windows\Fonts\Arial.ttf", size=30)
        draw.text((0, image.height+30),
                  f'{text_dict["score"]}\n{text_dict["evaluate"]}', fill=(0, 0, 0), font=font)

        save_file_path = get_save_file_path(
            rightfulness_dir_path, f'{index:0=3}.png')
        new_image.save(str(save_file_path))
