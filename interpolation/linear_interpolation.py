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

        # corner case here, if x_0 is fed in, i equals 0 but raise an error (since we use bisect_left)
        if target == self.x[0]:
            return self.y[0]

        if target < self.x[0] or target > self.x[-1]:
            raise MyError('Given target out of reach for linear interpolation')

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
        self.x = [86.03543, 81.03543, 76.03543, 61.03543, 50, 25, 10, 0, 5]
        self.y = [20.14, 18.64, 17.14, 15.64, 14.28, 15.04, 15.74, 17.14, 16.44]

        self.y = [i for i in self.y]
        self.li = Linear_itp(self.x, self.y)

    def test_init_(self):

        res_slopes = [-0.14, -0.14, -0.05, -0.03, 0.12, 0.10, 0.3, 0.3]

        self.assertEqual(res_slopes, [round(i, 2) for i in self.li.slopes], "slopes not right")

    def test_interpolate_general_case(self):

        case3 = 60

        case3_res = round(self.li.interpolate(case3), 4)
        case3_ans = 15.5124

        self.assertEqual(case3_res, case3_ans, "wrong trial with {}".format(case3))

        case4 = 80

        case4_res = round(self.li.interpolate(case4), 4)
        case4_ans = 18.3294

        self.assertEqual(case4_res, case4_ans, "wrong trial with {}".format(case4))

    def test_interpolate_corner_case(self):

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

        case5 = 0

        case5_res = round(self.li.interpolate(case5), 4)
        case5_ans = 17.14

        self.assertEqual(case5_res, case5_ans, "wrong trial with {}".format(case5))

        case6 = 86.03543

        case6_res = round(self.li.interpolate(case6), 4)
        case6_ans = 20.14

        self.assertEqual(case6_res, case6_ans, "wrong trial with {}".format(case6))

        case7 = 76.03543

        case7_res = round(self.li.interpolate(case7), 4)
        case7_ans = 17.14

        self.assertEqual(case7_res, case7_ans, "wrong trial with {}".format(case7))


if __name__ == "__main__":

    unittest.main()



