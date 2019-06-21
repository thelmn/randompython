from typing import Union
from decimal import Decimal

from my_math.gcd import gcd


class Fraction:
    def __init__(self, top: int, bottom: int):
        if bottom < 0:
            top = -top
            bottom = -bottom
        self.num = top
        self.den = bottom
        if top != 0:
            self.reduce()

    def reduce(self):
        g = gcd(self.den, self.num)
        if g > 1:
            self.den, self.num = self.den // g, self.num // g

    def reciprocate(self):
        self.num, self.den = self.den, self.num

    @property
    def reciprocal(self):
        return Fraction(self.den, self.num)

    @classmethod
    def create(cls, value: Union[int, float, 'Fraction']):
        if isinstance(value, int):
            return cls(value, 1)
        elif isinstance(value, float):
            dp = -Decimal(value).as_tuple().exponent
            if dp > 4:
                return cls(round(value * 10000), 10000)
            else:
                return cls(round(value * 10**dp), 10**dp)
        elif isinstance(value, Fraction):
            return value

    def __add__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        if isinstance(other, Fraction):
            return Fraction(self.num * other.den + other.num * self.den, self.den * other.den)
        else:
            raise ArithmeticError("Can only add to fraction or integer")

    def __radd__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        if isinstance(other, Fraction):
            return Fraction(self.num * other.den + other.num * self.den, self.den * other.den)
        else:
            raise ArithmeticError("Can only add to fraction or integer")

    def __sub__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        if isinstance(other, Fraction):
            return Fraction(self.num * other.den - other.num * self.den, self.den * other.den)
        else:
            raise ArithmeticError("Can only subtract to fraction or integer")

    def __mul__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        if isinstance(other, Fraction):
            return Fraction(self.num * other.num, self.den * other.den)
        else:
            raise ArithmeticError("Can only subtract to fraction or integer")

    def __rmul__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        if isinstance(other, Fraction):
            return Fraction(self.num * other.num, self.den * other.den)
        else:
            raise ArithmeticError("Can only subtract to fraction or integer")

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        if isinstance(other, Fraction):
            return Fraction(self.num * other.den, self.den * other.num)
        else:
            raise ArithmeticError("Can only subtract to fraction or integer")

    def __abs__(self):
        n, m = self.num, self.den
        if n < 0:
            n = -n
        return Fraction(n, m)

    def __eq__(self, other):
        return self.num * other.den == self.den * other.num

    def __lt__(self, other):
        return self.num / self.den < other.num / other.den

    def __gt__(self, other):
        return self.num / self.den > other.num / other.den

    def __repr__(self):
        if self.den == 1:
            return "{}".format(self.num)
        if self.num == 0:
            return "0"
        return "{}/{}".format(self.num, self.den)

if __name__ == "__main__":
    fr = Fraction(2, 3)
    print(fr)
    print(fr + 3)
    print(fr + Fraction(1, 2))
    print(fr - Fraction(1, 2))
    a = gcd(-9, 3)
    print(a)
    fr2 = Fraction(10, 1000)
    print(fr2 < fr)
    print(fr2 * fr)
    print(fr2 / fr)
    print(round(-2.134527 * 10000))
    print(Fraction.create(2.345678))
    print(Fraction(36, 12))

