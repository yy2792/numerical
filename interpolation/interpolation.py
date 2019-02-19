import unittest
from bisect import bisect_left


class Linear_itp():

    def __init__(self, x_, y_):
        temp = sorted(zip(x_, y_), key=lambda x: x[0])
        self.x = [float(i[0]) for i in temp]
        self.y = [float(i[1]) for i in temp]

        intervals = zip(self.x, self.x[1:], self.y, self.y[1:])
        self.slopes = [(y2 - y1) / (x2 - x1) for x1, x2, y1, y2 in intervals]

    def interpolate(self, target):

        i = bisect_left(self.x, target) - 1
        if i < 0 or i >= len(self.x):
            raise MyError('Index Error: The interpolated value must be between {} and {}'
                          .format(self.x[0], self.x[-1]))

        return self.y[i] + self.slopes[i] * (target - self.x[i])


class MyError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class testLinear_itp(unittest.TestCase):

    def setUp(self):
        self.x = [86.03543, 81.03543, 76.03543, 61.03543, 50, 25, 10, 5, 0]
        self.y = [20.14, 18.64, 17.14, 15.64, 14.28, 15.04, 15.74, 16.44, 17.14]
        self.y = [i for i in self.y]
        self.li = Linear_itp(self.x, self.y)

    def test_init_(self):

        res_slopes = [-0.14, -0.14, -0.05, -0.03, 0.12, 0.10, 0.3, 0.3]

        self.assertEqual(res_slopes, [round(i, 2) for i in self.li.slopes], "slopes not right")

    def test_interpolate(self):

        case1 = -2

        try:
            self.li.interpolate(case1)
        except MyError as er:
            self.assertEqual(er.message[:11], "Index Error")

        case2 = 90

        try:
            self.li.interpolate(case1)
        except MyError as er:
            self.assertEqual(er.message[:11], "Index Error")

        case3 = 60

        case3_res = round(self.li.interpolate(case3), 4)
        case3_ans = 15.5124

        self.assertEqual(case3_res, case3_ans, "wrong trial with {}".format(case3))

        case4 = 80

        case4_res = round(self.li.interpolate(case4), 4)
        case4_ans = 18.3294

        self.assertEqual(case4_res, case4_ans, "wrong trial with {}".format(case4))






