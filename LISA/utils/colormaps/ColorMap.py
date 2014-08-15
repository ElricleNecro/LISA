#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

# from PyQt4 import QtGui as Qt
from LISA.gui.utils.signals import Signal
from scipy.interpolate import InterpolatedUnivariateSpline

__all__ = [
    "ColorMap",
    "CubeHelix",
    "LinearInterpolation",
]


class ColorMap(object):
    """
    A class providing interface for colormaps. All of them must inherit it.
    """

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        if data is not None:
            self._data_min = data.min()
            self._data_max = data.max()
        else:
            self._data_min = 0.
            self._data_max = 1.

    def createWidget(self, parent):
        pass


class CubeHelix(ColorMap):

    __name__ = "CubeHelix"

    def __init__(self, data=None, hue=1.2, color=3., cycles=-1, gamma=1.):
        self.data = data
        self._hue = hue
        self._color = color
        self._cycles = cycles
        self._gamma = gamma
        self.changed = Signal()

    @property
    def hue(self):
        return self._hue

    @hue.setter
    def hue(self, hue):
        self._hue = hue
        self.changed()

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, gamma):
        self._gamma = gamma
        self.changed()

    @property
    def cycles(self):
        return self._cycles

    @cycles.setter
    def cycles(self, cycles):
        self._cycles = cycles
        self.changed()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.changed()

    def __call__(self, data):

        dg = (
            (data - self._data_min) / (self._data_max - self._data_min)
        ) ** self._gamma
        a = self._hue * dg * (1. - dg) / 2.
        phi = 2 * np.pi * (self._color / 3. + self._cycles * data)
        cosphi = a * np.cos(phi)
        sinphi = a * np.sin(phi)
        r = dg - 0.14861 * cosphi + 1.78277 * sinphi
        g = dg - 0.29227 * cosphi - 0.90649 * sinphi
        b = dg + 1.97249 * cosphi

        return np.vstack([r, g, b]).T.astype(np.float32).flatten()

    def createWidget(self, parent):

        # layout
        # layout = parent

        # # double spin boxes
        # layout.addWidget(Qt.QLabel("Hue"))
        # hue = Qt.QDoubleSpinBox()
        # hue.valueChanged[float].connect(self.set_hue)
        # layout.addWidget(hue)
        # layout.addWidget(Qt.QLabel("Gamma"))
        # gamma = Qt.QDoubleSpinBox()
        # gamma.valueChanged[float].connect(self.set_gamma)
        # layout.addWidget(gamma)
        # layout.addWidget(Qt.QLabel("Cycles"))
        # cycles = Qt.QDoubleSpinBox()
        # cycles.valueChanged[float].connect(self.set_cycles)
        # layout.addWidget(cycles)
        # layout.addWidget(Qt.QLabel("Color"))
        # color = Qt.QDoubleSpinBox()
        # color.valueChanged[float].connect(self.set_color)
        # layout.addWidget(color)

        # parent.addWidget(layout)
        pass

    def set_hue(self, value):
        self.hue = value

    def set_gamma(self, value):
        self.gamma = value

    def set_color(self, value):
        self.color = value

    def set_cycles(self, value):
        self.cycles = value


class LinearInterpolation(ColorMap):
    """
    A simple linear interpolation between two colors.
    """

    __name__ = "LinearInterpolation"

    def __init__(
        self,
        data,
        color_start=np.array([0., 0., 0.]),
        color_end=np.array([1., 1., 1.]),
    ):

        self.data = data
        self._color_start = color_start
        self._color_end = color_end
        self._interpolate()
        self.changed = Signal()

    @property
    def color_start(self):
        return self._color_start

    @color_start.setter
    def color_start(self, color_start):
        self._color_start = color_start
        self._interpolate()
        self.changed()

    @property
    def color_end(self):
        return self._color_end

    @color_end.setter
    def color_end(self, color_end):
        self._color_end = color_end
        self._interpolate()
        self.changed()

    def _interpolate(self):
        self._r = InterpolatedUnivariateSpline(
            [self._data_min, self._data_max],
            [self._color_start[0], self._color_end[0]],
            k=1,
        )
        self._g = InterpolatedUnivariateSpline(
            [self._data_min, self._data_max],
            [self._color_start[1], self._color_end[1]],
            k=1,
        )
        self._b = InterpolatedUnivariateSpline(
            [self._data_min, self._data_max],
            [self._color_start[2], self._color_end[2]],
            k=1,
        )

    def __call__(self, data):

        r = self._r(data)
        g = self._g(data)
        b = self._b(data)

        return np.vstack([r, g, b]).T.astype(np.float32).flatten()

    def createWidget(self, parent):

        pass
        # button_start = Qt.QPushButton("Start color")
        # button_start.clicked.connect(self._set_start_color)
        # parent.addWidget(button_start)

        # button_end = Qt.QPushButton("End color")
        # button_end.clicked.connect(self._set_end_color)
        # parent.addWidget(button_end)

    def _set_end_color(self):
        color = Qt.QColorDialog.getColor()
        self.color_end = [
            color.red() / 255.,
            color.green() / 255.,
            color.blue() / 255.
        ]

    def _set_start_color(self):
        color = Qt.QColorDialog.getColor()
        self.color_start = [
            color.red() / 255.,
            color.green() / 255.,
            color.blue() / 255.
        ]

# vim: set tw=79 :
