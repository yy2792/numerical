from root_solving.BS_formula import BS_Price, BS_Vega
import unittest
import copy

'''
json={
'S':xx, spot price
'K_low':xx, strike
'K_high':xx, strike
't':xx, time to maturity
'r':xx, interest rate
'q':xx, dividend
'vol':xx, volatility
}
'''


def helper_val(para_json, cp='c'):
    json_low = copy.deepcopy(para_json)
    json_low['K'] = json_low['K_low']

    json_high = copy.deepcopy(para_json)
    json_high['K'] = json_high['K_high']

    return BS_Price(json_low) - BS_Price(json_high)


def helper_d(para_json):
    json_low = copy.deepcopy(para_json)
    json_low['K'] = json_low['K_low']

    json_high = copy.deepcopy(para_json)
    json_high['K'] = json_high['K_high']

    return BS_Vega(json_low) - BS_Vega(json_high)


def newton(guess, target, para_json, cp='c', max_loop=1000, thred=10**(-8)):

    for i in range(max_loop):
        para_json['vol'] = guess
        guess_res = helper_val(para_json, cp=cp) - target
        guess_res_diff = helper_d(para_json)

        if abs(guess_res) < thred:
            return guess
        else:
            guess -= guess_res / guess_res_diff

    return None


def secant(guess1, guess2, target, para_json, cp='c', max_loop=1000, thred=10**(-8)):

    for i in range(max_loop):
        para_json['vol'] = guess1
        guess_res1 = helper_val(para_json, cp=cp) - target

        para_json['vol'] = guess2
        guess_res2 = helper_val(para_json, cp=cp) - target

        if abs(guess_res1) < thred:
            return guess1
        if abs(guess_res2) < thred:
            return guess2

        new_guess = (guess_res2 * guess1 - guess_res1 * guess2) / (guess_res2 - guess_res1)
        para_json['vol'] = new_guess
        new_guess_res = helper_val(para_json, cp=cp) - target

        if new_guess_res < thred:
            return new_guess

        if abs(new_guess - guess1) >= abs(new_guess - guess2):
            guess2 = guess1
            guess1 = new_guess
        else:
            guess1 = new_guess

    return None


def regula(guess1, guess2, target, para_json, cp='c', max_loop=1000, thred=10**(-8)):

    for i in range(max_loop):
        para_json['vol'] = guess1
        guess_res1 = helper_val(para_json, cp=cp) - target

        para_json['vol'] = guess2
        guess_res2 = helper_val(para_json, cp=cp) - target

        if abs(guess_res1) < thred:
            return guess1
        if abs(guess_res2) < thred:
            return guess2

        new_guess = (guess_res2 * guess1 - guess_res1 * guess2) / (guess_res2 - guess_res1)
        para_json['vol'] = new_guess
        new_guess_res = helper_val(para_json, cp=cp) - target

        if new_guess_res < thred:
            return new_guess

        if new_guess_res * guess_res1 < 0:
            guess2 = new_guess
        else:
            guess1 = new_guess

    return None


class MyError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class TestBS2(unittest.TestCase):

    def setUp(self):
        self.price_json = {
            'S': 120,
            'K_high': 122,
            'K_low':118,
            't': 92/365,
            'r': 0.005,
            'q': 0.04,
            'vol': 0.5
        }

    def test_newton(self):
        res = newton(0.2, 1.7, self.price_json)
        self.assertIsNone(res)

        res = newton(0.2, 1.6, self.price_json)
        self.assertEqual(0.9293, round(res, 4))

    def test_secant(self):
        res = secant(0.19, 0.2, 1.7, self.price_json)
        self.assertEqual(0.6394, round(res, 4))

        res = secant(0.19, 0.2, 1.6, self.price_json)
        self.assertEqual(0.9293, round(res, 4))

    def test_regula(self):
        res = regula(0.01, 0.3, 1.7, self.price_json)
        self.assertEqual(0.1066, round(res, 4))

        res = regula(0.01, 0.3, 1.6, self.price_json)
        self.assertEqual(0.0720, round(res, 4))

