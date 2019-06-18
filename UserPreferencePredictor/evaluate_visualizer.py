from GUI.image_canvas_frame import ImageCanvas
from tkinter import Tk, LEFT, Frame, Label, LabelFrame

from ImageEnhancer.util import get_image_enhancer

from UserPreferencePredictor.Model.util \
    import get_load_dir, MODEL_BUILDER_DICT, PREDICTABLE, \
    set_model_type_args, ArgumentParser
from ScoredParamIO.scored_param_reader import get_scored_param_list

class EvaluatedCanvasFrame(Frame):
    def __init__(self, master: Frame, canvas_width: int,
                 canvas_height: int, score: float, evaluate: float):
        super(EvaluatedCanvasFrame, self).__init__(master)
        self.canvas = ImageCanvas(self, canvas_width, canvas_height)

        self.canvas.pack()
        Label(self, text='score: %f' % (score)).pack()
        Label(self, text='evaluate: %.2f' % (evaluate)).pack()


if __name__ == "__main__":
    args = set_model_type_args(ArgumentParser()).parse_args()

    root = Tk()
    root.attributes('-topmost', True)

    root.withdraw()
    root.lift()
    root.focus_force()

    model_type = args.model_type

    try:
        load_dir = get_load_dir(model_type)
    except FileNotFoundError:
        print('ロード用フォルダが選択されなかったため終了します')
        exit()

    predict_model = MODEL_BUILDER_DICT[model_type][PREDICTABLE]()

    try:
        predict_model.restore(load_dir)
    except ValueError:
        print('ロードができなかったため終了します')
        exit()

    image_enhancer = get_image_enhancer()

    scored_param_list = get_scored_param_list()

    data_list = [
        {
            'image': image_enhancer.org_enhance(scored_param),
            'score': scored_param['score']}
        for scored_param in scored_param_list
    ]

    evaluate_list = predict_model.predict_evaluate(data_list).tolist()

    for i in range(len(data_list)):
        data_list[i]['evaluate'] = evaluate_list[i][0]

    high_predicted_data_list = \
        sorted(data_list, key=lambda x: x['evaluate'], reverse=True)

    high_scored_data_list = \
        sorted(data_list, key=lambda x: x['score'], reverse=True)

    root.deiconify()
    root.attributes('-topmost', True)

    disp_num = 4

    high_predict_frame = LabelFrame(root, text='predict')
    for predicted_data in high_predicted_data_list[:disp_num]:
        frame = \
            EvaluatedCanvasFrame(
                high_predict_frame, 300, 300, predicted_data['score'],
                predicted_data['evaluate'])
        frame.pack(side=LEFT)
        frame.canvas.update_image(predicted_data['image'])
    high_predict_frame.pack(pady=10)

    high_score_frame = LabelFrame(root, text='score')
    for scored_data in high_scored_data_list[:disp_num]:
        frame = \
            EvaluatedCanvasFrame(
                high_score_frame, 300, 300, scored_data['score'],
                scored_data['evaluate'])
        frame.pack(side=LEFT)
        frame.canvas.update_image(scored_data['image'])
    high_score_frame.pack(pady=10)

    root.mainloop()
