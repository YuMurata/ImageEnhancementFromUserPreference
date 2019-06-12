from deap import base, creator, tools, algorithms

from UserPreferencePredictor.Model.Compare.predictable_model \
    import PredictableModel
from UserPreferencePredictor.Model.util \
    import get_load_dir, select_model_type, UseType, MODEL_BUILDER_DICT

from ImageEnhancer.util import get_image_enhancer, ImageEnhancer
from ImageEnhancer.enhance_definer import enhance_name_list
import random
from statistics import mean, stdev
import numpy as np
from TrainDataGenerator.image_parameter_generator \
    import MIN_PARAM, MAX_PARAM

from tkinter import Tk, LEFT, Button, Frame, Toplevel

from GUI.image_canvas_frame import ImageCanvas

CANVAS_WIDTH, CANVAS_HEIGHT = 300, 300


class SelectableCanvasFrame(Frame):
    def __init__(self, master: Frame, enhancer: ImageEnhancer,
                 enhance_param: dict):

        super(SelectableCanvasFrame, self).__init__(master)

        self.canvas = ImageCanvas(self, CANVAS_WIDTH, CANVAS_HEIGHT)
        self.canvas.pack()
        Button(self, text='good', command=self._click_button).pack()

        self.enhancer = enhancer
        self.enhance_param = enhance_param

    def _click_button(self):
        self._param_update(self.enhance_param)

    def _param_update(self, org_enhance_param: dict):
        sub_win = Toplevel(self)
        sub_win.lift()

        gauss_param_list = []
        param_key_list = org_enhance_param.keys()
        param_list = org_enhance_param.values()

        mu = 1
        variation_width = 0.5
        sigma = variation_width/3

        disp_num = 4

        for i in range(disp_num):
            gauss_param = \
                [param*random.gauss(mu, sigma) for param in param_list]

            gauss_param_list.append(
                dict(zip(param_key_list, gauss_param)))

        for param in gauss_param_list:
            frame = \
                SelectableCanvasFrame(
                    sub_win, self.enhancer, self.enhance_param)
            frame.pack(side=LEFT)
            frame.canvas.update_image(self.enhancer.org_enhance(param))


def _init_model():
    model_type = select_model_type()
    model = MODEL_BUILDER_DICT[model_type][UseType.PREDICTABLE]()

    try:
        load_dir = get_load_dir(model_type)
    except FileNotFoundError:
        print('ロード用フォルダが選択されなかったため終了します')
        exit()

    try:
        model.restore(load_dir)
    except ValueError:
        print('学習済みモデルをロードできなかったため終了します')
        exit()

    return model


class ParameterOptimizer:
    def __init__(self, model: PredictableModel, image_enhancer: ImageEnhancer):
        self.image_enhancer = image_enhancer
        self.model = model
        self.toolbox = self._init_deap()

    def _decode_to_param(self, individual):
        quantize_param_list = \
            np.array_split(individual, len(enhance_name_list))
        bit_size = len(quantize_param_list[0])

        decoded_param_list = \
            [int(''.join(map(str, list(quantize_param))), 2)
             for quantize_param in quantize_param_list]

        normalized_param_list = \
            [x*(MAX_PARAM-MIN_PARAM)/(2**bit_size-1)+MIN_PARAM
             for x in decoded_param_list]

        return dict(zip(enhance_name_list, normalized_param_list))

    def _evaluate(self, individual):
        param = self._decode_to_param(individual)
        image = self.image_enhancer.resized_enhance(param)

        data = {'image': image}
        predict_evaluate = self.model.predict_evaluate([data]).tolist()[0][0]

        mu = 1
        variation_width = 0.5
        sigma = variation_width/3
        return predict_evaluate*random.gauss(mu, sigma),

    def _init_deap(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register(
            "individual", tools.initRepeat,
            creator.Individual, toolbox.attr_bool, 100)
        toolbox.register(
            "population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", self._evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        return toolbox

    def _individual_to_list(self, individual_tuple):
        individual_list = [ind[0] for ind in individual_tuple]
        return individual_list

    def optimize(self):
        random.seed(64)

        pop = self.toolbox.population(n=30)
        hof = tools.HallOfFame(1)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", lambda ind: mean(self._individual_to_list(ind)))
        stats.register("std", lambda ind: stdev(self._individual_to_list(ind)))
        stats.register("min", lambda ind: min(self._individual_to_list(ind)))
        stats.register("max", lambda ind: max(self._individual_to_list(ind)))

        algorithms.eaSimple(
            pop, self.toolbox, cxpb=0.5, mutpb=0.2,
            ngen=10, stats=stats, halloffame=hof)

        param_list = [self._decode_to_param(ind) for ind in hof]
        param_list.extend([self._decode_to_param(ind) for ind in pop[:3]])
        return param_list


if __name__ == "__main__":
    root = Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    root.lift()
    root.focus_force()

    model = _init_model()
    image_enhancer = get_image_enhancer()

    optimizer = ParameterOptimizer(model, image_enhancer)
    best_param_list = optimizer.optimize()
    print(best_param_list)

    for param in best_param_list:
        frame = SelectableCanvasFrame(root, image_enhancer, param)
        frame.pack(side=LEFT)
        frame.canvas.update_image(image_enhancer.org_enhance(param))

    root.deiconify()
    root.attributes('-topmost', False)
    root.lift()
    root.mainloop()
