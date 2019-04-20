import scipy.stats
import numpy as np
import math
import unittest

'''
json={
'S':xx, spot price
'K':xx, strike
't':xx, time to maturity
'r':xx, interest rate
'q':xx, dividend
'vol':xx, volatility
}
'''


def cdf_norm(x):
    return scipy.stats.norm(0, 1).cdf(x)


def BS_Price(para_json, cp='c'):

    S = float(para_json['S'])
    K = float(para_json['K'])
    t = float(para_json['t'])
    r = float(para_json['r'])
    q = float(para_json['q'])
    vol = float(para_json['vol'])

    d1 = (np.ln(S/K) + (r-q+pow(vol, 2)/2) * t) / (vol * np.sqrt(t))
    d2 = d1 - vol * np.sqrt(t)

    if cp == 'c':
        price = S * math.exp(-q*t) * cdf_norm(d1) - K * math.exp(-r*t)*cdf_norm(d2)
    else:
        price = K * math.sqrt(-r*t)*cdf_norm(-d2) - S * math.exp(-q*t)*cdf_norm(-d1)

    return price


class MyError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class testBS(unittest.TestCase):

    def setUp(self):