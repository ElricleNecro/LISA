#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import LISA.utils.colormaps as CM
import LISA.tools as t

from OpenGL import GL
from OpenGL.arrays import numpymodule
# from PyQt4 import QtGui as Qt
# from PyQt4 import QtCore

from LISA.Matrice import Vector
from LISA.gui.utils.signals import Signal
from .read_mock import ReadMock
from LISA.OpenGL import Shaders

numpymodule.NumpyHandler.ERROR_ON_COPY = True


class Mock(ReadMock):

    def __init__(self, *args, **kwargs):

        # set the reader
        super(Mock, self).__init__(*args, **kwargs)

        self._projections = ["Celestial sphere", "Redshift space", "Cartesian"]
        self.widgetChanged = Signal()
        self.widgetChanged.connect(self.updateWidget)

        # load data from mock catalogue
        self._load_data()

        # make cartesian projection by default
        self._projection_cartesian()

        # colormap
        colormap = getattr(CM, "LinearInterpolation")
        self._colormap = colormap(self._data[self._quantity].values)
        self._callback_colormap()
        self._colormap.changed.connect(self._callback_colormap)

        self._voxelSize = 0.01
        self._voxelSize_max = 0.05

        self._shaders = Shaders()
        self._shaders += t.shader_path("reader/mock/couleurs.vsh")
        self._shaders += t.shader_path("reader/mock/couleurs.fsh")

    def _callback_colormap(self):
        self._color = self._colormap(self._data[self._quantity].values)

    def _load_data(self):

        # store the data of the mock catalogue
        self._data = self.__call__(
            select="positions_x, positions_y, positions_z, alpha, delta, " +
            "redshift"
        )

        # rescale data
        for i in "xyz":
            field = "positions_{0}".format(i)
            self._data[field] = (
                self._data[field] - self._data[field].min()
            ) / (self._data[field].max() - self._data[field].min())

        field = "redshift"
        self._quantity = field
        self._data[field] = (
            self._data[field] - self._data[field].min()
        ) / (self._data[field].max() - self._data[field].min())

    def createShaders(self, parent):

        GL.glEnable(GL.GL_PROGRAM_POINT_SIZE)
        GL.glEnable(GL.GL_POINT_SPRITE)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glDepthMask(GL.GL_FALSE)

    def show(self, parent):

        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)

        matrice = parent._view * parent._model

        self._shaders.bind()
        self._shaders.setUniformValue("modelview", matrice)
        self._shaders.setUniformValue("projection", parent._projection)
        self._shaders.setUniformValue("screenSize", parent._screensize)
        self._shaders.setUniformValue("voxelSize", Vector(self._voxelSize))

        self._shaders.enableAttributeArray("position")
        self._shaders.setAttributeArray(
            "position",
            self._pos,
        )

        self._shaders.enableAttributeArray("color")
        self._shaders.setAttributeArray(
            "color",
            self._color,
        )

        GL.glDrawArrays(GL.GL_POINTS, 0, self._pos.shape[0] // 3)

        self._shaders.disableAttributeArray("position")
        self._shaders.disableAttributeArray("color")

        self._shaders.release()

    def createWidget(self, title="Mock catalogue controls", parent=None):
        pass

        # create a dialig window
        # self._dialog = Qt.QDialog(parent=parent)
        # self._dialog.setWindowOpacity(0.4)
        # self._dialog.setWindowTitle(title)

        # # set a layout
        # self._dialog.setLayout(Qt.QVBoxLayout())

        # self.updateWidget()

        # return self._dialog

    def updateWidget(self):
        pass

        # get the layout and clear children
        # try:
            # layout = self._dialog.layout()
            # while layout.takeAt(0):
                # child = layout.takeAt(0)
                # del child
        # except:
            # pass

        # # create a slider
        # slider = Qt.QSlider(QtCore.Qt.Horizontal)
        # slider.valueChanged[int].connect(self._set_voxelsize)

        # # add a label for slider and the slider
        # self._dialog.layout().addWidget(
            # Qt.QLabel("Point size")
        # )
        # self._dialog.layout().addWidget(slider)

        # # create a list of projections
        # combo = Qt.QComboBox()
        # for projection in self._projections:
            # combo.addItem(projection)
        # self._dialog.layout().addWidget(
            # Qt.QLabel("Kind of projections")
        # )
        # combo.activated[str].connect(self._projection_changed)
        # self._dialog.layout().addWidget(combo)

        # # get the quantity to color
        # self._dialog.layout().addWidget(Qt.QLabel("Colormap quantity"))
        # lineInput = Qt.QLineEdit()

        # def _getText():
            # text = lineInput.text()
            # self._load_quantity(text)
        # lineInput.returnPressed.connect(_getText)
        # self._dialog.layout().addWidget(lineInput)

        # # create a list of colormaps
        # combomap = Qt.QComboBox()
        # for colormap in CM.ColorMap.__subclasses__():
            # combomap.addItem(colormap.__name__)
        # self._dialog.layout().addWidget(
            # Qt.QLabel("Kind of colormap")
        # )
        # combomap.activated[str].connect(self._colormap_changed)
        # self._dialog.layout().addWidget(combomap)

        # # add the widget of the colormap
        # self._dialog.layout().addWidget(
            # Qt.QLabel("Colormap controls")
        # )
        # self._colormap.createWidget(self._dialog.layout())

    def _load_quantity(self, quantity):
        if quantity not in self._data:
            try:
                self._data[quantity] = self.__call__(select=quantity)
                self._quantity = quantity
                self._colormap.data = self._data[self._quantity].values
                self._callback_colormap()
            except:
                pass

    def _colormap_changed(self, text):

        # get the new colormap
        colormap = getattr(CM, text)
        self._colormap = colormap(self._data[self._quantity].values)
        self._callback_colormap()
        self._colormap.changed.connect(self._callback_colormap)
        self.widgetChanged()

    def _projection_changed(self, text):

        # get the method to call according to the projection
        projection = text.lower().replace(" ", "_")
        method = getattr(self, "_projection_" + projection)
        method()

    def _projection_celestial_sphere(self):
        X = np.cos(self._data["alpha"]) * np.cos(self._data["delta"])
        Y = np.sin(self._data["alpha"]) * np.cos(self._data["delta"])
        Z = np.sin(self._data["delta"])
        self._pos = np.vstack([X, Y, Z]).T.astype(np.float32).flatten()

    def _projection_cartesian(self):
        self._pos = np.vstack([
            self._data["positions_x"].values,
            self._data["positions_y"].values,
            self._data["positions_z"].values,
        ]).T.astype(np.float32).flatten()

    def _projection_redshift_space(self):
        redshift = self._data["redshift"]
        X = np.cos(self._data["alpha"]) * np.cos(self._data["delta"])
        Y = np.sin(self._data["alpha"]) * np.cos(self._data["delta"])
        Z = np.sin(self._data["delta"])
        self._pos = np.vstack(
            [
                redshift * X,
                redshift * Y,
                redshift * Z
            ]
        ).T.astype(np.float32).flatten()

    def _set_voxelsize(self, value):
        self._voxelSize = value / 100. * self._voxelSize_max

# vim: set tw=79 :
