from deap import base, creator, tools, algorithms

from UserPreferencePredictor.Model.Compare.ranknet import RankNet

from ImageEnhancer.image_enhancer import ImageEnhancer
from ImageEnhancer.enhance_definer import enhance_name_list
import random
from statistics import mean, stdev
import numpy as np
from TrainDataGenerator.image_parameter_generator \
    import MIN_PARAM, MAX_PARAM


class ParameterOptimizer:
    def __init__(self, model: RankNet, image_enhancer: ImageEnhancer):
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
        predict_evaluate = self.model.predict([data]).tolist()[0][0]

        mu = 1
        variation_width = 0.5
        sigma = variation_width/3
        return predict_evaluate*random.gauss(mu, sigma),

    def _init_deap(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register("individual", tools.initRepeat,
                         creator.Individual, toolbox.attr_bool, 100)
        toolbox.register("population", tools.initRepeat,
                         list, toolbox.individual)

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
            ngen=300, stats=stats, halloffame=hof)

        param_list = [self._decode_to_param(ind) for ind in hof]
        param_list.extend([self._decode_to_param(ind) for ind in pop[:3]])
        return param_list
