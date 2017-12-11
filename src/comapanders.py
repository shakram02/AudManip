import math


class Compander:
    def encode(self, sample):
        raise NotImplementedError()

    def decode(self, sample):
        raise NotImplementedError()


class ALawCompander(Compander):
    def __init__(self, A):
        self._A = A
        self._A_INV = 1.0 / self._A
        self._ONE_PLUS_LN_A = 1.0 + math.log(self._A)
        self._sign = lambda x: math.copysign(1, x)

    def encode(self, sample):
        abs_x = math.fabs(sample)

        if abs_x < self._A_INV:
            # ( A * |X| ) / (1 + ln(A)) 0<= |X| <= 1/A
            y = self._A * abs_x / self._ONE_PLUS_LN_A
        else:
            # ( sign(x) *(1 + ln(A * |X|)) / (1 + ln(A)) 1/A<= |X| <= 1
            y = (1.0 + math.log(self._A * abs_x)) / self._ONE_PLUS_LN_A

        sampled = self._sign(sample) * y
        return sampled, (sample - sampled) ** 2

    def decode(self, sample):
        pass


class MLawCompander(Compander):
    def __init__(self, M):
        self._M = M
        self._LN_ONE_PLUS_M = math.log(1.0 + self._M)
        self._sign = lambda x: math.copysign(1, x)

    def encode(self, sample):
        # f(x) = (sign(x)*ln(1+ m*|x|)) / ln(1+m)
        abs_x = math.fabs(sample)
        y = math.log(1 + self._M * abs_x) / self._LN_ONE_PLUS_M

        sampled = self._sign(sample) * y
        return sampled, (sample - sampled) ** 2

    def decode(self, sample):
        pass
