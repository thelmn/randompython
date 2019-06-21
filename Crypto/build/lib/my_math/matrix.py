import copy
from typing import Union

from my_math.fraction import Fraction


class Matrix:

    class Cursor:
        def __init__(self, h: int, w: int):
            self._h = h
            self._w = w
            self._p = 1
            self._q = 1

        def left(self):
            if self._q == self._w:
                self.down()
                self._q = 1
            else:
                self._q += 1

        def right(self):
            if self._q == 1:
                self.up()
                self._q = self._w
            else:
                self._q -= 1

        def down(self):
            if self._p == self._h:
                self._p = 1
            else:
                self._p += 1

        def up(self):
            if self._p == 1:
                self._p = self._h
            else:
                self._p -= 1

        def to_row(self, p: int):
            if p > self._h:
                raise IndexError("Cursor row position out of bound")
            else:
                self._p = p

        def to_col(self, q: int):
            if q > self._w:
                raise IndexError("Cursor column position out of bound")
            else:
                self._q = q

        def to(self, p: int, q: int):
            self.to_row(p)
            self.to_col(q)

        @property
        def at(self):
            return self._p - 1, self._q - 1

    class SizeError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    def __init__(self, rows: int, cols: int):
        self._i = rows
        self._j = cols
        self._matrix = Matrix.zero([rows, cols])
        self.c = self.Cursor(rows, cols)

    def insert(self, value: int):
        value = Fraction.create(value)
        p = self.c.at
        self._matrix[p[0]][p[1]] = value
        self.c.left()

    def insert_at(self, value: int, row: int, col: int):
        self.c.to(row, col)
        self.insert(value)

    def insert_row(self, row: list):
        row = [Fraction.create(x) for x in row]
        p = self.c.at
        if len(row) > self._j:
            row = row[:self._j]
        elif len(row) < self._j:
            row += [Fraction.create(0) for i in range(self._j - len(row))]
        self._matrix[p[0]] = row
        self.c.down()

    def insert_row_at(self, row: list, pos: int):
        self.c.to_row(pos)
        self.insert_row(row)

    def same_order(self, other: 'Matrix'):
        return (self._i, self._j) == (other._i, other._j)

    def cross_order(self, other: 'Matrix'):
        return self._j == other._i

    def is_square(self):
        return self._i == self._j

    def _check_index(self, p: int, q: int):
        if p > self._i or p == 0:
            raise IndexError("Row index out of bound")
        elif q > self._j or q == 0:
            raise IndexError("Column index out of bound")
        else:
            return True

    def del_row(self, i):
        if i > self._i or i < 1:
            raise IndexError("Row index out of bound")
        else:
            i -= 1
            self._matrix.pop(i)
            self._i -= 1

    def del_col(self, j):
        if j > self._j or j < 1:
            raise IndexError("Column index out of bound")
        else:
            j -= 1
            for row in self._matrix:
                row.pop(j)
            self._j -= 1

    def trim(self, i: int, j: int):
        self.del_row(i)
        self.del_col(j)

    def trimmed(self, pos):
        i, j = pos
        mat = copy.deepcopy(self)
        mat.trim(i, j)
        return mat

    def _det(self, m: 'Matrix'):
        if len(m) == 1:
            return m[1, 1]
        else:
            s = 1
            d = 0
            for i in range(1, m._j + 1):
                d += s * m[1, i] * self._det(m.trimmed([1, i]))
                s *= -1
            return d

    def cofactor(self, i: int, j: int):
        self._check_index(i, j)
        s = -1
        if (i+j) % 2 == 0:
            s = 1
        return self._det(self.trimmed([i, j])) * s


    @property
    def inverse(self):
        return self.adjoint / abs(self.det)

    @property
    def adjoint(self):
        return self.cofactor_matrix.transpose

    @property
    def cofactor_matrix(self):
        mat = [[self.cofactor(i, j) for j in range(1, self._j+1)] for i in range(1, self._i+1)]
        return Matrix.create(mat)

    @property
    def det(self):
        if self.is_square():
            return self._det(self)
        else:
            raise ArithmeticError("Attempting to get the determinant of a non-square matrix")

    @property
    def transpose(self):
        return Matrix.create([[row[i] for row in self._matrix] for i in range(self._j)])

    @property
    def size(self):
        return self._i, self._j

    @property
    def matrix(self):
        return self._matrix

    @classmethod
    def create(cls, matrix: list):
        m = cls(len(matrix), len(matrix[0]))
        m._matrix = [[Fraction.create(x) for x in row] for row in matrix]
        return m

    @staticmethod
    def zero(size):
        p, q = size
        return [[Fraction.create(0) for j in range(q)] for i in range(p)]

    @classmethod
    def identity(cls, size: int):
        i = cls(size, size)
        for x in range(1, size+1):
            i[x, x] = 1
        return i

    def __add__(self, other: 'Matrix'):
        if self.same_order(other):
            return Matrix.create([[sum(x) for x in zip(*row)] for row in zip(*(self._matrix, other.matrix))])
        else:
            raise ArithmeticError("Attempting to add matrices of different order")

    def __sub__(self, other: 'Matrix'):
        if self.same_order(other):
            other *= -1
            return Matrix.create([[sum(x) for x in zip(*row)] for row in zip(*(self._matrix, other.matrix))])
        else:
            raise ArithmeticError("Attempting to subtract matrices of different order")

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.cross_order(other):
                a = [(rows, cols) for rows in self._matrix for cols in other.transpose.matrix]
                a = [[(r*c) for r, c in zip(*row)] for row in a]
                a = [sum(p) for p in a]
                return Matrix.create([[a[(j + i*other._j)] for j in range(other._j)] for i in range(self._i)])
            else:
                raise ArithmeticError("Attempting to multiply matrices with different column and row")
        elif isinstance(other, int) or isinstance(other, float):
            return Matrix.create([[x * other for x in row] for row in self._matrix])
        else:
            raise TypeError("Can only multiply with matrix or integer or float")

    def __truediv__(self, other: Union[int, float, 'Fraction']):
        frac = Fraction.create(other)
        frac.reciprocate()
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Fraction):
            return Matrix.create([[frac * x for x in row] for row in self._matrix])
        else:
            raise TypeError("Can only divide with matrix or integer or float")

    def __neg__(self):
        return self * -1

    def __iter__(self):
        for i in range(self._i):
            for j in range(self._j):
                yield self[i+1, j+1]

    def __getitem__(self, index):
        p, q = index
        if self._check_index(p, q):
            return self._matrix[p-1][q-1]

    def __setitem__(self, key, value):
        p, q = key
        self.c.to(p, q)
        self.insert(value)

    def __len__(self):
        return self._i * self._j

    def __repr__(self):
        text = "Matrix({}, {})\n".format(self._i, self._j)
        for p in range(self._i):
            for q in range(self._j):
                text += "{} ".format(self._matrix[p][q])
            text += "\n"
        return text

if __name__ == "__main__":
    m = Matrix(5, 5)
    print(m)
    m.insert(5)
    m.insert_at(7, 2, 3)
    print(m)
    m.insert_row([1, 2, 3, 4])
    print(m)
    m.insert_row_at([4, 3, 2], 4)
    print("matrix")
    print(m)
    print("transpose")
    print(m.transpose)
    print("addition")
    print(m + m)
    print("subtraction")
    print(m - m)
    print("product")
    print(m * 10)
    print("matrix product")
    print(m * m.transpose)
    a = [[1, 2, 3], [1, 3, 5], [1, 5, 12]]
    a = Matrix.create(a)
    print(a)
    print(a.cofactor(1, 1))
    print("cofactor")
    print(a.cofactor_matrix)
    print("adjoint")
    print(a.adjoint)
    print("inverse")
    print(a.inverse)
    print("abs det")
    print(abs(a.det))
    print(a.inverse * a)

