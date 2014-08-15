#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import numpy as np
import LISA.tools.common as c

from OpenGL import GL
from OpenGL.arrays import numpymodule

numpymodule.NumpyHandler.ERROR_ON_COPY = True

from .Reader import GadgetReader
from LISA.OpenGL import Shaders as s
from LISA import Matrice as m


class Sprites(GadgetReader):

    def __init__(self, *args, **kwargs):
        super(Sprites, self).__init__(*args, **kwargs)
        self.Read()
        self._pos = self.positions
        # self._pos = self.positions.astype(np.float64)

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
        GL.glEnable(GL.DEPTH_TEST)

    def show(self, parent):

        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)

        matrice = parent._view * parent._model

        self._shaders.bind()
        self._shaders.setUniformValue("modelview", matrice)
        self._shaders.setUniformValue("projection", parent._projection)
        self._shaders.setUniformValue("screenSize", parent._screensize)
        self._shaders.setUniformValue("voxelSize", m.Vector(0.01))

        self._shaders.enableAttributeArray("position")

        self._shaders.setAttributeArray("position", self._pos)

        GL.glDrawArrays(GL.GL_POINTS, 0, self._pos.shape[0] // 3)

        self._shaders.disableAttributeArray("position")

        self._shaders.release()

    def _push_button(self):
        pass

# vim: set tw=79 :
