import unittest
import numpy as np


def inverse_triang(mx):

    '''
    :param mx: 2D array (triangular matrix)
    :return: 2D array
    '''

    '''
    [[1, 3, 0, 0],
     [2. 2, 3, 0],
     [0, 1, 2, 3],
     [0, 0, 2, 1]]
    '''


def upper_triangle(mx, flag=1):

    #if it cannot be reduced to an upper triangle, return -1

    def helper(mx, line_num):

        n = len(mx)

        if flag == 1:
            # enable row number check (we have to assume matrix is n * 2n here
            if len(mx[0]) != 2 * n:
                raise MyError('The col number should be twice of row number')
                return -1

        if n == 1:
            t = mx[0][0]
            for i in range(2):
                mx[0][i] /= t

            return mx

        # we do not expect a non-zero number in diagonal
        if mx[line_num][line_num] == 0:
            return -1

        t = mx[line_num][line_num]

        # base case, line_num == n - 1, everything before should be 0
        for i in range(line_num):
            if mx[line_num][i] != 0:
                return -1

        if t != 1:
            # if pivot is not 1
            for i in range(line_num, len(mx[0])):
                mx[line_num][i] /= t

        # now deduce each row with multiple of first row
        for i in range(line_num + 1, n):
            first_item = mx[i][line_num]
            for j in range(line_num, len(mx[0])):
                mx[i][j] -= first_item * mx[line_num][j]

        if line_num == n - 1:
            return mx

        return helper(mx, line_num + 1)

    return helper(mx, 0)


class Cubic_itp():

    def __init__(self, x_, y_, condition='n', head=0, tail=0):

        # condition is n (natural), s (slope), sfs, sff, ...

        temp = sorted(zip(x_, y_), key=lambda x: -x[0])
        self.x = [float(i[0]) for i in temp]
        self.y = [float(i[1]) for i in temp]
        self.condition = condition
        self.head = 0
        self.tail = 0

    def cubic_fit(self):

        x_intervals = zip(self.x, self.x[1:])
        # h starts at 1, h1 = x1 - x0, add 0 to the front to make the index consistent
        h = [0] + [(x2 - x1) for x1, x2 in x_intervals]

        h_intervals = zip(h[1:], h[2:])
        # phi starts with p1, ....
        phi = [h2 / (h1 + h2) for h1, h2 in h_intervals]

        mu = [0] + [(1 - p) for p in phi]

        d_intervals = zip(self.y, self.y[1:], self.y[2:], h[1:], h[2:])

        # this starts with d1, d1 = 6 / (h1 + h2) * ((y2-y1) / h2 - (y1 - y0) / h1)
        d = [(6 / (h2 + h3)) * ((y3 - y2) / h3 - (y2 - y1) / h2) for y1, y2, y3, h2, h3 in d_intervals]

        if self.condition == 'n':
            phi = [0] + phi
            mu = mu + [0]
            d = [0] + d + [0]

        else:
            if self.condition[0] == 'f':
                phi = [1] + phi
                d0 = (6 / h[1]) * ((y[1] - y[0]) / h[1] - self.head)
                d = [d0] + d

            elif self.condition[0] == 's':
                phi = [0] + phi
                d0 = 2 * self.head
                d = [d0] + d

            if self.condition[1] == 'f':
                mu = mu + [1]
                dn = 6 / h[-1] * (self.tail - (self.y[-1] - self.y[-2]) / h[-1])
                d = d + [dn]

            elif self.condition[1] == 's':
                mu = mu + [0]
                dn = 2 * self.tail
                d = d + [dn]

        # set up the matrix

        length = len(self.x)

        temp_matrix = [[0 for i in range(length)] for j in range(length)]

        for i in range(length):
            temp_matrix[i][i] = 2
            if i < length - 1:
                temp_matrix[i][i + 1] = phi[i]
                temp_matrix[i + 1][i] = mu[i + 1]

        # easy way

        temp_martix = np.array(temp_matrix)
        d = np.array(d)
        m = np.linalg.solve(temp_matrix, d)

        print(m)

        # end



class MyError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class testCubic_itp(unittest.TestCase):

    def setUp(self):
        self.x = [86.03543, 81.03543, 76.03543, 61.03543, 50, 25, 10, 0, 5]
        self.y = [20.14, 18.64, 17.14, 15.64, 14.28, 15.04, 15.74, 17.14, 16.44]

        self.ci = Cubic_itp(self.x, self.y)

    def test_cubic_fit(self):
        self.ci.cubic_fit()

        self.y = [21.14, 18.64, 17.14, 15.64, 14.28, 15.04, 15.74, 17.14, 16.44]

        self.ci = Cubic_itp(self.x, self.y)

        self.ci.cubic_fit()


class test_inverse_triang(unittest.TestCase):

    def setUp(self):
        self.mx = [[1, 3, 0, 0], [2, 2, 3, 0], [0, 1, 2, 3], [0, 0, 2, 1]]

    def test_upper_triangle(self):

        mx1 = [[2, 3]]
        res = upper_triangle(mx1)

        self.assertEqual(res, [[1, 1.5]])

        mx2 = [[3, 2, 1], [2, 1, 1], [0, 2, 3]]
        t_res = [[1, 2/3, 1/3], [0, 1, -1], [0, 0, 1]]

        res = upper_triangle(mx2, 0)
        np.testing.assert_almost_equal(res, t_res, 5)

        mx2_new = [[3, 2, 1, 1, 0, 0], [2, 1, 1, 0, 1, 0], [0, 2, 3, 0, 0, 1]]
        res2 = upper_triangle(mx2_new)

        t_res2 = [[1, 2/3, 1/3, 1/3, 0, 0], [0, 1, -1, 2, -3, 0], [0, 0, 1, -0.8, 1.2, 0.2]]

        np.testing.assert_almost_equal(res2, t_res2, 5)



