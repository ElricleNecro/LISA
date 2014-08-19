#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import datetime

from OpenGL import GL
from OpenGL.arrays import numpymodule

import LISA.tools as t

from LISA.OpenGL import Buffer, INDEX_BUFFER, VERTEX_BUFFER
from LISA.OpenGL import Shaders as s
from LISA.Matrice import Vector

numpymodule.NumpyHandler.ERROR_ON_COPY = True


class Rippler(object):

    def __init__(self, *args, **kwargs):

        # create mesh
        self.npoints = 30
        X = np.linspace(-1, 1, self.npoints)
        Y = np.linspace(-1, 1, self.npoints)
        Z = np.zeros(self.npoints, dtype=np.float32)
        x, y, z = np.meshgrid(X, Y, Z)
        self._mesh = np.array([x, y, z], dtype=np.float32).T.flatten()

        # create the indices for triangles
        self._indices = np.empty(
            (self.npoints - 1, self.npoints - 1, 6),
            dtype=np.uint32
        )
        indices = np.array(range(self.npoints - 1), dtype=np.uint32)
        for i in range(self.npoints - 1):
            self._indices[i, :, 0] = indices[:] + i * self.npoints
            self._indices[i, :, 1] = indices[:] + 1 + i * self.npoints
            self._indices[i, :, 2] = indices[:] + (i + 1) * self.npoints
            self._indices[i, :, 3] = indices[:] + (i + 1) * self.npoints
            self._indices[i, :, 4] = indices[:] + 1 + (i + 1) * self.npoints
            self._indices[i, :, 5] = indices[:] + 1 + i * self.npoints
        self._indices = self._indices.flatten()

        self._time = datetime.datetime.now()

    def createShaders(self, parent):

        self._shaders = s.CreateShaderFromFile(
            t.shader_path("rippler/rippler.vsh")
        ) + s.CreateShaderFromFile(
            t.shader_path("rippler/rippler.fsh")
        )

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        self._shaders.link()

        # create buffers
        self._vertices = Buffer(VERTEX_BUFFER)
        self._index = Buffer(INDEX_BUFFER)
        self._vertices.create()
        self._index.create()

        # allocate buffers
        self._vertices.bind()
        self._vertices.allocate(
            self._mesh,
            len(self._mesh) * 4
        )
        self._vertices.release()
        self._index.bind()
        self._index.allocate(
            self._indices,
            len(self._indices) * 4
        )
        self._index.release()

    def show(self, parent):
        self._shaders.bind()

        self._shaders.setUniformValue(
            "modelview",
            parent._projection * parent._view * parent._model
        )
        dt = datetime.datetime.now() - self._time
        second = float((dt.seconds * 1000000 + dt.microseconds) * 0.000006)
        self._shaders.setUniformValue("time", Vector(second, dtype=np.float32))

        self._vertices.bind()
        self._shaders.enableAttributeArray("in_Vertex")
        self._shaders.setAttributeBuffer(
            "in_Vertex",
            self._mesh,
        )
        self._vertices.release()

        self._index.bind()
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            6 * (self.npoints - 1) ** 2,
            GL.GL_UNSIGNED_INT,
            None
        )
        self._index.release()

        self._shaders.disableAttributeArray("in_Vertex")
        self._shaders.release()

# vim: set tw=79 :
