import unittest


class Poly_itp():

    def __init__(self, x_, y_):
        temp = sorted(zip(x_, y_), key=lambda x: x[0])
        self.x = [float(i[0]) for i in temp]
        self.y = [float(i[1]) for i in temp]

    def interpolate_func(self, target, x, y):

        nv_matrix = [[None for i in range(len(x) + 1)] for j in range(len(x))]

        for i in range(len(x)):
            nv_matrix[i][0] = x[i]
            nv_matrix[i][1] = y[i]

        def helper(i, j):

            if i < 0 or i > len(nv_matrix) or j < 0 or j > len(nv_matrix[0]):
                return None

            if nv_matrix[i][j] is not None:
                return nv_matrix[i][j]

            upper = nv_matrix[i][0]
            lower = nv_matrix[i + j - 1][0]

            helper(i + 1, j - 1)
            helper(i, j - 1)

            nv_matrix[i][j] = ((target - upper) * nv_matrix[i+1][j-1] - (target - lower) * nv_matrix[i][j-1]) / (lower - upper)

        helper(0, len(x))

        self.print_matrix(nv_matrix)

        return nv_matrix[0][-1]

    def interpolate(self, target):

        return self.interpolate_func(target, self.x[:], self.y[:])

    def interpolate_rev(self, target):

        return self.interpolate_func(target, self.x[::-1], self.y[::-1])

    def print_matrix(self, mx):

        for i in range(len(mx)):
            temp_x = [round(x, 4) for x in mx[i] if x is not None]
            print(temp_x)


class MyError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class testPoly_itp(unittest.TestCase):

    def setUp(self):
        self.x = [86.03543, 81.03543, 76.03543, 61.03543, 50, 25, 10, 0, 5]
        self.y = [20.14, 18.64, 17.14, 15.64, 14.28, 15.04, 15.74, 17.14, 16.44]

        self.y = [i for i in self.y]
        self.li = Poly_itp(self.x, self.y)

    def test_interpolate_general_case(self):

        case1 = 45

        case1_res = self.li.interpolate(case1)
        case1_ans = 13.81027

        self.assertEqual(case1_ans, round(case1_res, 5), "wrong trial with {}".format(case1))

        case2_res = self.li.interpolate_rev(case1)
        case2_ans = 13.81027

        self.assertEqual(case2_ans, round(case2_res, 5), "wrong trial with {}".format(case1))

        case3 = 90

        case3_res = self.li.interpolate(case3)
        case3_ans = 19.20794

        self.assertEqual(case3_ans, round(case3_res, 5), "wrong trial with {}".format(case3))


if __name__ == "__main__":

    unittest.main()
