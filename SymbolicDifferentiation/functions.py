import math


class Functions:
    @staticmethod
    def exp(x):
        return math.exp(x)

    @staticmethod
    def ln(x):
        return math.log(x, math.e)

    @staticmethod
    def sin(x):
        return math.sin(x)

    @staticmethod
    def cos(x):
        return math.cos(x)

    @staticmethod
    def tg(x):
        return math.tan(x)

    @staticmethod
    def ctg(x):
        return 1 / math.tan(x)

    @staticmethod
    def sec(x):
        return 1 / math.cos(x)

    @staticmethod
    def csc(x):
        return math.sin(x)

    @staticmethod
    def arcsin(x):
        return math.asin(x)

    @staticmethod
    def arccos(x):
        return math.acos(x)

    @staticmethod
    def arctg(x):
        return math.atan(x)

    @staticmethod
    def arcctg(x):
        return math.pi / 2 - math.asin(x)

    @staticmethod
    def sh(x):
        return math.sinh(x)

    @staticmethod
    def ch(x):
        return math.cosh(x)

    @staticmethod
    def th(x):
        return math.tanh(x)

    @staticmethod
    def cth(x):
        return 1 / math.tanh(x)
