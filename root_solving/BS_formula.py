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

def pdf_norm(x):
    return scipy.stats.norm(0, 1).pdf(x)

def BS_Price(para_json, cp='c'):
    S = float(para_json['S'])
    K = float(para_json['K'])
    t = float(para_json['t'])
    r = float(para_json['r'])
    q = float(para_json['q'])
    vol = float(para_json['vol'])

    d1 = (np.log(S / K) + (r - q + pow(vol, 2) / 2) * t) / (vol * np.sqrt(t))
    d2 = d1 - vol * np.sqrt(t)

    if cp == 'c':
        price = S * math.exp(-q * t) * cdf_norm(d1) - K * math.exp(-r * t) * cdf_norm(d2)
    elif cp == 'p':
        price = K * math.exp(-r * t) * cdf_norm(-d2) - S * math.exp(-q * t) * cdf_norm(-d1)
    else:
        raise MyError('type should be c or p')

    return price

def BS_Vega(para_json):
    S = float(para_json['S'])
    K = float(para_json['K'])
    t = float(para_json['t'])
    r = float(para_json['r'])
    q = float(para_json['q'])
    vol = float(para_json['vol'])

    d1 = (np.log(S / K) + (r - q + pow(vol, 2) / 2) * t) / (vol * np.sqrt(t))
    v = S * math.sqrt(t) * math.exp(-q*t) * pdf_norm(d1)
    return v


class MyError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class TestBS(unittest.TestCase):

    def setUp(self):
        self.price_json = {
            'S': 31.55,
            'K': 22.75,
            't': 3.5,
            'r': 0.05,
            'q': 0.02,
            'vol': 0.5
        }

    def testBS_price(self):
        c = BS_Price(self.price_json)
        self.assertEqual(14.73, round(c, 2))

        p = BS_Price(self.price_json, cp='p')
        self.assertEqual(4.41, round(p, 2))

    def testVega(self):
        v = BS_Vega(self.price_json)
        self.assertEqual(14.25, round(v, 2))

