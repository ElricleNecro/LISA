#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import numpy as np
import LISA.tools.tools as c

from OpenGL import GL
from OpenGL.arrays import numpymodule

numpymodule.NumpyHandler.ERROR_ON_COPY = True

from .Reader import GadgetReader
from LISA import Object as o
from LISA import Matrice as m


class Simu(o.Base):

    def __init__(self, filename, **kwargs):
        if "numfile" in kwargs:
            num = kwargs["numfile"]
            del kwargs["numfile"]
        else:
            num = 1
        fich = GadgetReader(filename, num)
        fich.Read()

        self._sigma = 0.2
        self._size = 0.01
        self._cut_off = 0.25

        super(Simu, self).__init__(fich.positions, **kwargs)

        self._shaders += c.shader_path("halo/halo.vsh")
        self._shaders += c.shader_path("halo/halo.fsh")

    def createShaders(self, parent):
        self._shaders.link()

        GL.glEnable(GL.GL_PROGRAM_POINT_SIZE)
        GL.glEnable(GL.GL_POINT_SPRITE)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_BLEND)
        # GL.glEnable(GL.DEPTH_TEST)

    def show(self, parent):

        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)

        matrice = parent._view * self._model

        self._shaders.bind()
        self._shaders.setUniformValue("modelview", matrice)
        self._shaders.setUniformValue("projection", parent._projection)
        self._shaders.setUniformValue("screenSize", parent._screensize)
        self._shaders.setUniformValue("voxelSize", m.Vector(self._size))
        self._shaders.setUniformValue("sigma", m.Vector(self._sigma))
        self._shaders.setUniformValue("cut_off", m.Vector(self._cut_off))

        self._shaders.enableAttributeArray("position")

        self._shaders.setAttributeArray("position", self.data)

        GL.glDrawArrays(GL.GL_POINTS, 0, self.data.shape[0] // 3)

        self._shaders.disableAttributeArray("position")

        self._shaders.release()

# vim: set tw=79 :
