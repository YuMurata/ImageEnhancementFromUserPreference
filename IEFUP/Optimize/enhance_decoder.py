from IEFUP.submodule import ParameterOptimizer
import numpy as np
import IEFUP.ImageEnhancer as IE


class EnhanceDecorder(ParameterOptimizer.BitDecoder):
    def decode(self, bit_list: list):
        quantize_param_list = \
            np.array_split(bit_list, len(IE.enhance_name_list))
        bit_size = len(quantize_param_list[0])

        decoded_param_list = \
            [int(''.join(map(str, list(quantize_param))), 2)
             for quantize_param in quantize_param_list]

        normalized_param_list = \
            [x*(IE.MAX_PARAM-IE.MIN_PARAM)/(2**bit_size-1)+IE.MIN_PARAM
             for x in decoded_param_list]

        return dict(zip(IE.enhance_name_list, normalized_param_list))
