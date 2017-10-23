import math


class Compander:
    def encode(self, sound_data):
        result = []
        error = 0

        for sample in sound_data:
            quantized, sample_err = self._encode_sample(sample)
            result.append(quantized)
            error += sample_err ** 2

        return result, error

    def _encode_sample(self, sample):
        raise NotImplementedError()


class ALawCompander(Compander):
    def __init__(self, A):
        self._A = A
        self._A_INV = 1.0 / self._A
        self._ONE_PLUS_LN_A = 1.0 + math.log(self._A)
        self._sign = lambda x: math.copysign(1, x)

    def _encode_sample(self, x):
        abs_x = math.fabs(x)

        if abs_x < self._A_INV:
            # ( A * |X| ) / (1 + ln(A)) 0<= |X| <= 1/A
            y = self._A * abs_x / self._ONE_PLUS_LN_A
        else:
            # ( sign(x) *(1 + ln(A * |X|)) / (1 + ln(A)) 1/A<= |X| <= 1
            y = (1.0 + math.log(self._A * abs_x)) / self._ONE_PLUS_LN_A

        sampled = self._sign(x) * y
        return sampled, (x - sampled) ** 2


class MLawCompander(Compander):
    def __init__(self, M):
        self._M = M
        self._LN_ONE_PLUS_M = math.log(1.0 + self._M)
        self._sign = lambda x: math.copysign(1, x)

    def _encode_sample(self, x):
        # f(x) = (sign(x)*ln(1+ m*|x|)) / ln(1+m)
        abs_x = math.fabs(x)
        y = math.log(1 + self._M * abs_x) / self._LN_ONE_PLUS_M

        sampled = self._sign(x) * y
        return sampled, (x - sampled) ** 2
