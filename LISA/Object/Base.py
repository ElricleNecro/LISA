#!/usr/bin/env python
# encoding: utf-8

import numpy as np

import LISA.tools.common as c
import LISA.Matrice as m

from LISA.OpenGL import Shaders as s
from OpenGL import GL


__all__ = [
        "Point",
        "Lines",
        "TriangleMesh",
        "QuadMesh",
        "Base",
]


class Point(object):
    def __call__(self, data):
        GL.glDrawArrays(GL.GL_POINTS, 0, data.shape[0] // 3)


class Lines(object):
    def __init__(self, ids=None, data=None):
        if (ids is None) and (data is not None):
            l = len(data.flatten()) // 3
            self._ids = np.array(
                    range(l),
                    dtype=np.uint32,
            )
            # self._ids = np.repeat(
                    # range(l+1),
                    # 2
            # )[1:-3]
            # self._ids[-1] = 0
            # print(l, len(self._ids))
        else:
            self._ids = ids

    def __call__(self, data):
        GL.glDrawElements(
            GL.GL_LINE_STRIP,
            len(self._ids),
            GL.GL_UNSIGNED_INT,
            self._ids
        )


class TriangleMesh(object):
    def __init__(self, ids=None, data=None, side_x=30, side_y=30):
        if (ids is None) and (data is not None):
            # create the indices for triangles
            self._ids = np.empty(
                (side_x - 1, side_y - 1, 6),
                dtype=np.uint32
            )
            indices = np.array(range(side_x - 1), dtype=np.uint32)
            for i in range(side_y - 1):
                self._ids[:, i, 0] = indices[:] + i * side_y
                self._ids[:, i, 1] = indices[:] + 1 + i * side_y
                self._ids[:, i, 2] = indices[:] + (i + 1) * side_y
                self._ids[:, i, 3] = indices[:] + (i + 1) * side_y
                self._ids[:, i, 4] = indices[:] + 1 + (i + 1) * side_y
                self._ids[:, i, 5] = indices[:] + 1 + i * side_y
            self._ids = self._ids.flatten()
        else:
            self._ids = ids

    def __call__(self, data):
        # GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._ids),
            # 6 * (self._len - 1) ** 2,
            GL.GL_UNSIGNED_INT,
            self._ids
        )


class QuadMesh(object):
    def __init__(self, ids=None, data=None, side_x=30, side_y=30):
        if (ids is None) and (data is not None):
            # create the indices for triangles
            self._ids = np.empty(
                (side_x - 1, side_y - 1, 4),
                dtype=np.uint32
            )
            indices = np.array(range(side_x - 1), dtype=np.uint32)
            for i in range(side_y - 1):
                self._ids[:, i, 0] = indices[:] + i * side_y
                self._ids[:, i, 1] = indices[:] + 1 + i * side_y
                self._ids[:, i, 2] = indices[:] + 1 + (i + 1) * side_y
                self._ids[:, i, 3] = indices[:] + (i + 1) * side_y
            self._ids = self._ids.flatten()
        else:
            self._ids = ids

    def __call__(self, data):
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glDrawElements(
            GL.GL_QUADS,
            len(self._ids),
            GL.GL_UNSIGNED_INT,
            self._ids
        )


class Base(object):
    def __init__(self, data, linetype=Point()):
        self.data = data

        self._model = m.Identity()

        self._plot_prop = linetype

    def createShaders(self, parent):
        self._shaders = s.CreateShaderFromFile(
            c.os.path.join(
                c.SHADERS_DIR,
                "basic.vsh"
            )
        ) + s.CreateShaderFromFile(
            c.os.path.join(
                c.SHADERS_DIR,
                "basic.fsh"
            )
        )

        self._shaders.link()

    def show(self, parent):
        GL.glEnable(GL.GL_DEPTH_TEST)

        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)

        matrice = parent._view * self._model

        self._shaders.bind()
        self._shaders.setUniformValue("modelview", matrice)
        self._shaders.setUniformValue("projection", parent._projection)

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

    def __lshift__(self, inst):
        self._plot_prop = inst



