#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import LISA.common as c

#from PyQt5.QtGui import *
#from PyQt4.QtOpenGL import QGLBuffer as QOpenGLBuffer
from PyQt4 import QtGui as Qt
from OpenGL import GL
from OpenGL.arrays import numpymodule

numpymodule.NumpyHandler.ERROR_ON_COPY = True

from .Reader import GadgetReader
from LISA import Shaders as s
from LISA import Matrice as m


class ShadersNotLinked(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class Sprites(GadgetReader):

    def __init__(self, *args, **kwargs):
        super(Sprites, self).__init__(*args, **kwargs)
        self.Read()
        self._pos = self.positions
        # self._pos = self.positions.astype(np.float64)

    def createShaders(self, parent):

        print("In CreateShaders")
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
        print("In CreateShaders")

        self._shaders.link()

        GL.glEnable(GL.GL_PROGRAM_POINT_SIZE)
        GL.glEnable(GL.GL_POINT_SPRITE)
        GL.glEnable(GL.DEPTH_TEST)

    def show(self, parent):

        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)

        matrice = parent._view * parent._model

        self._shaders.bind()
        self._shaders.setUniformValue("modelview", matrice)
        self._shaders.setUniformValue("projection", parent._projection)
        self._shaders.setUniformValue("screenSize", parent._screensize)
        self._shaders.setUniformValue("voxelSize", m.Vector(0.01))

        # vertex_id = self._shaders.attributeLocation("position")
        #color_id = self._shaders.attributeLocation("in_Color")

        self._shaders.enableAttributeArray("position")
        #self._shaders.enableAttributeArray("in_Color")

        self._shaders.setAttributeArray("position", self._pos)
        # GL.glVertexAttribPointer(
            # vertex_id,
            # 3,
            # GL.GL_DOUBLE,
            # GL.GL_FALSE,
            # 0,
            # self._pos
        # )

        GL.glDrawArrays(GL.GL_POINTS, 0, self._pos.shape[0] // 3)

        self._shaders.disableAttributeArray("position")
        #self._shaders.disableAttributeArray("in_Color")

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
