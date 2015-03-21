#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import LISA.Matrice as m
import math as mm


__all__ = ["Perspective", "Orthographic"]


class Perspective(m.Matrix):

    def __init__(self, *args, **kwargs):
        super(Perspective, self).__init__(*args, **kwargs)

        self._angle = 60.0
        self._ratio = 16 / 9
        self._minimal = 0.001
        self._maximal = 10000000.0
        self._setf()
        self[:] = m.Perspective(
            self._angle,
            self._ratio,
            self._minimal,
            self._maximal,
        )[:]

    def _setf(self):
        self._f = 1. / mm.tan(self._angle / 2.0 * mm.pi / 180.)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self._setf()
        self[0, 0] = self._f / self._ratio
        self[1, 1] = self._f

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, ratio):
        self._ratio = ratio
        self[0, 0] = self._f / self._ratio

    @property
    def minimal(self):
        return self._minimal

    @minimal.setter
    def minimal(self, minimal):
        self._minimal = minimal
        self[2, 2] = (
            self._minimal + self._maximal
        ) / (self._minimal - self._maximal)
        self[2, 3] = 2. * self._minimal * self._maximal / (
            self._minimal - self._maximal
        )

    @property
    def maximal(self):
        return self._maximal

    @maximal.setter
    def maximal(self, maximal):
        self._maximal = maximal
        self[2, 2] = (
            self._minimal + self._maximal
        ) / (self._minimal - self._maximal)
        self[2, 3] = 2. * self._minimal * self._maximal / (
            self._minimal - self._maximal
        )


class Orthographic(m.Matrix):

    def __init__(self, *args, **kwargs):
        super(Orthographic, self).__init__(*args, **kwargs)

        self._far = 10.
        self._near = -10
        self._right = 800.
        self._left = 0.
        self._top = 0.
        self._bottom = 800.
        self[:] = m.Orthographic(
            self._right,
            self._left,
            self._top,
            self._bottom,
            self._near,
            self._far,
        )[:]

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        self._right = right
        tmp = self._right - self._left
        self[0, 0] = 2. / tmp
        self[0, 3] = - (self._right + self._left) / tmp

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        self._left = left
        tmp = self._right - self._left
        self[0, 0] = 2. / tmp
        self[0, 3] = - (self._right + self._left) / tmp

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, top):
        self._top = top
        tmp = self._top - self._bottom
        self[1, 1] = 2. / tmp
        self[1, 3] = - (self._top + self._bottom) / tmp

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, bottom):
        self._bottom = bottom
        tmp = self._top - self._bottom
        self[1, 1] = 2. / tmp
        self[1, 3] = - (self._top + self._bottom) / tmp

    @property
    def far(self):
        return self._far

    @far.setter
    def far(self, far):
        self._far = far
        tmp = self._far - self._near
        self[2, 2] = - 2. / tmp
        self[2, 3] = (self._far + self._near) / tmp

    @property
    def near(self):
        return self._near

    @near.setter
    def near(self, near):
        self._near = near
        tmp = self._far - self._near
        self[2, 2] = - 2. / tmp
        self[2, 3] = (self._far + self._near) / tmp

# vim: set tw=79 :
