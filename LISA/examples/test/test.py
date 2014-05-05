#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import LISA.common as c

from PyQt4 import QtGui as Qt
from OpenGL import GL
from OpenGL.arrays import numpymodule

import LISA.Shaders as s
from LISA.Matrice import Vector

numpymodule.NumpyHandler.ERROR_ON_COPY = True


class ShadersNotLinked(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class Sprites(object):

    def __init__(self, *args, **kwargs):
        npoints = 10000
        rand = np.random.rand(npoints, 3)
        self._color = np.random.rand(npoints, 3).flatten()

        r = rand[:, 0] ** (1. / 3.)
        thet = np.arccos(2 * rand[:, 1] - 1)
        phi = 2. * np.pi * rand[:, 2]

        self._pos = np.array(
            [
                r * np.cos(phi) * np.sin(thet),
                r * np.sin(phi) * np.sin(thet),
                r * np.cos(thet)
            ],
            dtype=np.float32,
        ).T.flatten()

    def createShaders(self, parent):

        self._shaders = s.CreateShaderFromFile(
            c.os.path.join(
                c.SHADERS_DIR,
                "couleurs.vsh"
            )
        ) + s.CreateShaderFromFile(
            c.os.path.join(
                c.SHADERS_DIR,
                "couleurs.fsh"
            )
        )

        self._shaders.link()

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
        self._shaders.setUniformValue("voxelSize", Vector(0.01))

        self._shaders.enableAttributeArray("position")
        self._shaders.setAttributeArray(
            "position",
            self._pos,
        )

        GL.glDrawArrays(GL.GL_POINTS, 0, self._pos.shape[0] // 3)

        self._shaders.disableAttributeArray("position")

        self._shaders.release()

    def createWidget(self, title="Dialogue de test.", parent=None):
        dialog = Qt.QDialog(parent=parent)
        dialog.setWindowOpacity(0.4)
        dialog.setWindowTitle(title)
        dialog.setLayout(Qt.QVBoxLayout())
        dialog.layout().addWidget(
            Qt.QLabel("Ceci est un test d'affichage des widgets.")
        )
        dialog.layout().addWidget(
            Qt.QLabel("Ceci est un test d'affichage des widgets.")
        )
        but = Qt.QPushButton()
        but.setText("Un bouton !")
        but.clicked.connect(self._push_button)
        dialog.layout().addWidget(but)

        return dialog

    def _push_button(self):
        pass

# vim: set tw=79 :
