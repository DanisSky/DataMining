from copy import deepcopy


class Matrix:
    def __init__(self, list_of_lists):
        self.matrix = deepcopy(list_of_lists)
        self.i = len(list_of_lists)
        self.j = len(list_of_lists[0])

    def __getitem__(self, idx):

        return self.matrix[idx]

    def __add__(self, other):
        other = Matrix(other)
        result = []
        numbers = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                summa = other[i][j] + self.matrix[i][j]
                numbers.append(summa)
                if len(numbers) == len(self.matrix):
                    result.append(numbers)
                    numbers = []

        return Matrix(result)

    def __pow__(self, other):
        result = self
        for i in range(other - 1):
            result *= self

        return result

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            result = [[other * x for x in y] for y in self.matrix]

            return Matrix(result)

        elif self.j != other.i:

            return 'Different lengths of vectors'

        else:
            a = range(self.j)
            b = range(self.i)
            c = range(other.j)
            result = []
            for i in b:
                res = []
                for j in c:
                    el, m = 0, 0
                    for k in a:
                        m = self.matrix[i][k] * other.matrix[k][j]
                        el += m
                    res.append(el)
                result.append(res)

            return Matrix(result)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return '\n'.join('\t'.join(map(str, row))
                         for row in self.matrix)

    def sum_of_columns(self):
        result = []
        for vector in zip(*self.matrix):
            result.append(sum(vector))

        return result
    
    def size(self):

        return self.i, self.j

    @staticmethod
    def fill(n, value):
        list_ = []
        for i in range(n):
            list_.append([value])

        return Matrix(list_)
