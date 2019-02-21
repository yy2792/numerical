import unittest


class Cubic_itp():

    def __init__(self, x_, y_, condition='n'):

        # condition is n (natural), s (slope), sfs, sff, ...

        temp = sorted(zip(x_, y_), key=lambda x: -x[0])
        self.x = [float(i[0]) for i in temp]
        self.y = [float(i[1]) for i in temp]

    def cubic_fit(self):

        x_intervals = zip(self.x, self.x[1:])
        # h starts at 1, h1 = x1 - x0
        h = [0] + [(x2 - x1) for x1, x2 in x_intervals]

        h_intervals = zip(h[1:], h[2:])
        # phi starts with p1, ....
        phi = [h2 / (h1 + h2) for h1, h2 in h_intervals]

        mu = [(1 - p) for p in phi]

        d_intervals = zip(self.y, self.y[1:], self.y[2:], h[1:], h[2:])

        # this starts with d1, d1 = 6 / (h1 + h2) * ((y2-y1) / h2 - (y1 - y0) / h1)
        d = [(6 / (h2 + h3)) * ((y3 - y2) / h3 - (y2 - y1) / h2) for y1, y2, y3, h2, h3 in d_intervals]

        


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



