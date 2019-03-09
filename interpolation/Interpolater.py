import numpy as np
import matplotlib.pyplot as plt


class Interpolator(object):
    def __init__(self, _x, _y):
        self.x = None
        self.y = None
        self._name = 'General Interpolator'

    def interpolate(self, target):
        pass

    def plot(self, dots=300):

        temp = sorted(zip(self.x, self.y), key=lambda x: -x[0])
        plot_x = [float(i[0]) for i in temp]

        axis_x = np.linspace(plot_x[0], plot_x[-1], dots)

        vf = np.vectorize(lambda t: self.interpolate(t))

        axis_y = vf(axis_x)

        plt.plot(axis_x, axis_y, color='green', linewidth = 2)

        plt.title('{} interpolation'.format(self._name))

        plt.show()