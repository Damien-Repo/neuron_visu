#!/usr/bin/env python

import numpy as np

class Point():

    R = 8

    # F(x) = A * x + B
    A = 1.
    B = .0

    def __init__(self, x=None, y=None):
        if x == None: x = np.random.uniform(-1, 1)
        if y == None: y = np.random.uniform(-1, 1)

        assert x >= -1. and x <= 1.
        assert y >= -1. and y <= 1.
        self._x = x
        self._y = y

        if (self._y > self.F(self._x)):
            self.label = 1.
        else:
            self.label = -1.

        self._was_found = False

    @staticmethod
    def set_equation_F(a, b):
        assert a >= -1. and a <= 1.
        assert b >= -1. and b <= 1.
        Point.A = a
        Point.B = b

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def was_found(self):
        return self._was_found

    @staticmethod
    def F(x):
        return Point.A * x + Point.B

    @property
    def inputs(self):
        return np.array([self._x, self._y])

    def found(self, was_found=True):
        self._was_found = was_found
