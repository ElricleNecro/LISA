#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import LISA.Matrice as m
import math as mm


__all__ = ["Perspective"]


class Perspective(m.Matrix):

    def __init__(self, *args, **kwargs):
        super(Perspective, self).__init__(*args, **kwargs)

        self._angle = 60.0
        self._ratio = 16 / 9
        self._minimal = 0.000001
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

# vim: set tw=79 :
