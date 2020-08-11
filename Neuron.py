#!/usr/bin/env python

import numpy as np

class Neuron():

    def __init__(self):
        size = 2
        self.W = np.random.uniform(-1, 1, size)
        self.bias = np.random.uniform(-1, 1)

    @staticmethod
    def _activation(value):
        if value < 0.:
            return -1.
        return 1.

    def forward(self, X):
        assert isinstance(X, np.ndarray)
        value = sum(self.W * X) + self.bias
        return self._activation(value)

    def train(self, X, expected, training_rate=.00001):
        error = expected - self.forward(X)
        for i in range(len(self.W)):
            v = X[i] * error * training_rate
            self.W[i] += v

        self.bias += error * training_rate

    def F_a(self):
        return - self.W[0] / self.W[1]

    def F_b(self):
        return - self.bias / self.W[1]

    def F(self, x):
        '''
        wx = self.W[0]
        wy = self.W[1]
        wb = self.bias
        wx * x + wy * y + wb = 0
        wy * y = - wb - wx * x
        y = (- wb - wx * x) / wy
        y = (-wx/wy) * x + (-wb/wy)

        y = ax + b
        a = - wx / wy
        b = - wb / wy
        '''
        y = self.F_a() * x + self.F_b()
        return y
