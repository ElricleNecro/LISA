#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import datetime

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o

from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER
from LISA.Matrice import Vector
from LISA.gui.widget import Widget


class Rippler(o.Base):

    def __init__(self, *args, **kwargs):

        npoints = 30
        X = np.linspace(-1, 1, npoints).astype(np.float32)
        Y = np.linspace(-1, 1, npoints).astype(np.float32)
        Z = np.zeros((npoints,npoints), dtype=np.float32)
        x, y = np.meshgrid(X, Y)
        mesh = np.vstack((x, y, Z)).reshape(3, -1).T.astype(np.float32)

        super(Rippler, self).__init__(mesh, linetype=o.TriangleMesh(data=mesh))

        self._widget = Widget()

        self._shaders += t.shader_path("rippler/rippler.vsh")
        self._shaders += t.shader_path("rippler/rippler.fsh")

        self._time = datetime.datetime.now()

    def createShaders(self, parent):

        # create buffers
        self._vertices = VBO(VERTEX_BUFFER)
        self._index = VBO(INDEX_BUFFER)
        self._vao = VAO()

        self._vertices.create()
        self._index.create()
        self._vao.create()

        # allocate buffers
        self._vertices.bind()
        self._vertices.allocate(
            self._data,
            len(self._data) * 4
        )
        self._vertices.release()
        self._index.bind()
        self._index.allocate(
            self._plot_prop._ids,
            len(self._plot_prop._ids) * 4
        )
        self._index.release()

        self._shaders.build()
        self._shaders.bindAttribLocation("position")

        self._shaders.link()

        self._vao.bind()

        self._index.bind()
        self._vertices.bind()

        self._shaders.enableAttributeArray("position")
        self._shaders.setAttributeBuffer(
            "position",
            self._data,
        )

        self._vao.release()

        # create shaders for widget
        self._widget.createShaders()

    def createWidget(self):
        return self._widget

    def show(self, parent):

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        self._shaders.bind()

        self._shaders.setUniformValue(
            "projection",
            parent._projection
        )
        self._shaders.setUniformValue(
            "modelview",
            parent._view * self._model
        )
        dt = datetime.datetime.now() - self._time
        second = float((dt.seconds * 1000000 + dt.microseconds) * 0.000006)
        self._shaders.setUniformValue("time", Vector(second, dtype=np.float32))

        self._vao.bind()

        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._plot_prop._ids),
            GL.GL_UNSIGNED_INT,
            None,
        )

        self._vao.release()

        self._shaders.release()

# vim: set tw=79 :
