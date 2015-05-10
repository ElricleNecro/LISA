#!/usr/bin/env python
# encoding: utf-8

import numpy as np

import LISA.tools as t
import LISA.Matrice as m

from .Meshtype import Point
from LISA.OpenGL import Shaders
from OpenGL import GL


__all__ = [
    "Base",
]


class Base(object):
    def __init__(self, data, linetype=Point(), shaders=None):
        self.data = data

        self._model = m.Identity()

        self._plot_prop = linetype

        self._shaders = Shaders()
        if shaders is not None:
            for v in shaders:
                self._shaders += v

    def createShaders(self, world):
        if len(self._shaders) == 0:
            self._shaders += t.shader_path("basic.vsh")
            self._shaders += t.shader_path("basic.fsh")
        self._shaders.link()

    def paintEvent(self, event):
        GL.glEnable(GL.GL_DEPTH_TEST)

        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)

        matrice = self.world._view * self._model

        self._shaders.bind()
        self._shaders.setUniformValue("modelview", matrice)
        self._shaders.setUniformValue("projection", self.world._projection)

        self._shaders.enableAttributeArray("position")

        self._shaders.setAttributeArray("position", self._data)

        self._plot_prop(self._data)

        self._shaders.disableAttributeArray("position")

        self._shaders.release()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        if len(val.shape) != 1:
            self._data = val.flatten()
        else:
            self._data = val

    @property
    def model(self):
        return self._model
    @model.setter
    def model(self, model):
        self._model = model

    @property
    def shaders(self):
        return self._shaders

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, world):
        self._world = world

    def __lshift__(self, inst):
        self._plot_prop = inst


# vim: set tw=79 :
