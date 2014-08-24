#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from OpenGL import GL
from OpenGL.arrays import numpymodule

import LISA.OpenGL.Shaders as s
import LISA.tools as t
import LISA.Matrice as m

from LISA.Matrice import Vector

numpymodule.NumpyHandler.ERROR_ON_COPY = True


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

        self._model = m.Identity()

    def createShaders(self, parent):

        self._shaders = s.CreateShaderFromFile(
            t.shader_path("sprite/sprite.vsh")
        ) + s.CreateShaderFromFile(
            t.shader_path("sprite/sprite.fsh")
        )

        self._shaders.link()

        GL.glEnable(GL.GL_PROGRAM_POINT_SIZE)
        GL.glEnable(GL.GL_POINT_SPRITE)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glDepthMask(GL.GL_FALSE)

    def show(self, parent):

        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)

        matrice = parent._view * self._model

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

    def _push_button(self):
        pass

# vim: set tw=79 :
