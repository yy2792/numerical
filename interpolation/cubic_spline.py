import unittest
import numpy as np
from bisect import bisect_left
from interpolation.Interpolater import Interpolator


def reverse_bisect_left(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x > a[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo - 1


def inverse_matrix(mx):

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

    if len(mx) != len(mx[0]):
        raise MyError('matrix is not square matrix')

    id_mx = np.identity(len(mx))

    new_mx = np.concatenate((np.array(mx), id_mx), axis=1)

    up_mx = upper_triangle(new_mx)
    low_mx = lower_triangle(up_mx)

    inv_mx = low_mx[:, len(low_mx):]

    return inv_mx


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


def lower_triangle(mx, flag=1):

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

        # we do expect a non-zero number in diagonal
        if mx[line_num][line_num] == 0:
            return -1

        t = mx[line_num][line_num]

        # base case, line_num == n - 1, everything after should be 0
        for i in range(line_num + 1, n):
            if mx[line_num][i] != 0:
                return -1

        if t != 1:
            # if pivot is not 1
            for i in range(len(mx[0])):
                mx[line_num][i] /= t

        # now deduce each row with multiple of first row
        for i in range(line_num):
            first_item = mx[i][line_num]
            for j in range(len(mx[0])):
                mx[i][j] -= first_item * mx[line_num][j]

        if line_num == 0:
            return mx

        return helper(mx, line_num - 1)

    return helper(mx, len(mx) - 1)


class Cubic_itp(Interpolator):

    def __init__(self, x_, y_, condition='n', head=0, tail=0, order='ASC'):

        super().__init__(x_, y_)

        self._name = 'cubic'

        # condition is n (natural), ff (slope), ss (second), sf, fs, ...
        if condition not in ['n', 'ff', 'ss', 'fs', 'sf']:
            raise MyError('Invalid 2 degrees of freedom')

        self.order = order

        if order == 'DESC':
            temp = sorted(zip(x_, y_), key=lambda x: -x[0])
        elif order == 'ASC':
            temp = sorted(zip(x_, y_), key=lambda x: x[0])
        else:
            raise MyError('order should be asc or desc')

        self.x = [float(i[0]) for i in temp]
        self.y = [float(i[1]) for i in temp]
        self.condition = condition
        self.head = head
        self.tail = tail
        self.para = None

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
                d0 = (6 / h[1]) * ((self.y[1] - self.y[0]) / h[1] - self.head)
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

        # a_i ()^3 + b_i ()^2 + c_i () + d_i
        # calculate ai
        ai_interval = zip(m, m[1:], h[1:])
        ai = [(m2 - m1)/(6 * h) for m1, m2, h in ai_interval]

        # calculate bi
        bi = [m_i / 2 for m_i in m[:-1]]

        # calculate ci
        ci_interval = zip(self.y[1:], self.y, m[1:], m, h[1:])
        ci = [(y2 - y1) / h2 - ((m2 + 2 * m1) / 6) * h2 for y2, y1, m2, m1, h2 in ci_interval]

        # calculate di
        di = [yi for yi in self.y[:-1]]

        self.para = list(zip(ai, bi, ci, di))

        # end

    def interpolate(self, target):

        if self.para is None:
            self.cubic_fit()
            if self.para is None:
                raise MyError('cannot fit and get paras for given input')

        if target < min(self.x) or target > max(self.x):
            raise MyError('target value is out of reach')

        if target == self.x[0]:
            return self.y[0]

        if target == self.x[-1]:
            return self.y[-1]

        if self.order == 'ASC':
            i = bisect_left(self.x, target) - 1
        else:
            i = reverse_bisect_left(self.x, target)

        if i < 0 or i >= len(self.x):
            raise MyError('Index Error: The interpolated value must be between {} and {}'
                          .format(self.x[0], self.x[-1]))

        ai, bi, ci, di = self.para[i]
        temp_x = self.x[i]

        return ai * pow((target - temp_x), 3) + bi * pow((target - temp_x), 2) + ci * (target - temp_x) + di


class MyError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class testCubic_itp(unittest.TestCase):

    def setUp(self):
        self.x = [86.03543, 81.03543, 76.03543, 61.03543, 50, 25, 10, 0, 5]
        self.y = [20.14, 18.64, 17.14, 15.64, 14.28, 15.04, 15.74, 17.14, 16.44]
        #self.y = [y / 100 for y in self.y]

        self.ci = Cubic_itp(self.x, self.y, order='DESC')

    def test_cubic_fit(self):
        self.ci.cubic_fit()

        res = round(self.ci.interpolate(45), 4)
        self.assertEqual(res, 14.0425)

        x = reversed(self.x)
        y = reversed(self.y)

        self.ci = Cubic_itp(x, y)
        self.ci.cubic_fit()

        res2 = round(self.ci.interpolate(45), 4)
        self.assertEqual(res, res2)

    def test_cubic_fit_natural(self):
        self.ci = Cubic_itp(self.x, self.y, order='DESC')
        self.ci.cubic_fit()

        self.assertEqual(round(self.ci.interpolate(40), 4), 14.1289)

        for i in range(len(self.x)):
            self.assertEqual(round(self.ci.interpolate(self.x[i]), 4), round(self.y[i], 4))

        self.ci = Cubic_itp(self.x, self.y, order='ASC')
        self.ci.cubic_fit()

        self.assertEqual(round(self.ci.interpolate(40), 4), 14.1289)

        for i in range(len(self.x)):
            self.assertEqual(round(self.ci.interpolate(self.x[i]), 4), round(self.y[i], 4))

    def test_cubic_fit_other(self):
        self.ci = Cubic_itp(self.x, self.y, condition='ss', head=5, tail=5, order='ASC')
        self.ci.cubic_fit()
        self.assertEqual(round(self.ci.interpolate(45), 4), 14.1638)

        self.ci = Cubic_itp(self.x, self.y, condition='ff', head=5, tail=5, order='ASC')
        self.ci.cubic_fit()
        self.assertEqual(round(self.ci.interpolate(45), 4), 13.6580)




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

    def test_lower_triangle(self):

        mx1 = [[2, 3]]
        res = lower_triangle(mx1)

        self.assertEqual(res, [[1, 1.5]])

        mx2 = [[3, 2, 1], [2, 1, 1], [0, 2, 3]]
        t_res = [[1, 0, 0], [5.999999, 1, 0], [0, 2/3, 1]]

        res = lower_triangle(mx2, 0)
        np.testing.assert_almost_equal(res, t_res, 5)

        mx2_new = [[3, 2, 1, 1, 0, 0], [2, 1, 1, 0, 1, 0], [0, 2, 3, 0, 0, 1]]
        res2 = lower_triangle(mx2_new)

        t_res2 = [[1, 0, 0, -0.2, 0.8, -0.2], [6, 1, 0, 0, 3, -1], [0, 2/3, 1, 0, 0, 1/3]]

        np.testing.assert_almost_equal(res2, t_res2, 5)

    def test_inverse_matrix(self):

        mx = np.array([[3, 2, 1], [2, 1, 1], [0, 2, 3]])

        inv_mx = inverse_matrix(mx)

        np.testing.assert_almost_equal(np.dot(mx, inv_mx), np.identity(len(mx)))

        mx2 = np.array([[1, 5, 6], [2, 3, 3], [1, 10, 3]])

        inv_mx2 = inverse_matrix(mx2)

        np.testing.assert_almost_equal(np.dot(mx2, inv_mx2), np.identity(len(mx2)))


class test_reverse_bisect_left(unittest.TestCase):

    def setUp(self):
        self.rev_sample = [86, 81, 76, 61, 50, 25, 10, 5, 0]

    def test_func(self):

        self.assertEqual(self.rev_sample[reverse_bisect_left(self.rev_sample, 60)], 61)
        self.assertEqual(self.rev_sample[reverse_bisect_left(self.rev_sample, 61)], 61)
        self.assertEqual(self.rev_sample[reverse_bisect_left(self.rev_sample, 0)], 0)
        self.assertEqual(self.rev_sample[reverse_bisect_left(self.rev_sample, 80)], 81)
        self.assertEqual(self.rev_sample[reverse_bisect_left(self.rev_sample, 86)], 86)


if __name__ == '__main__':

    unittest.main()