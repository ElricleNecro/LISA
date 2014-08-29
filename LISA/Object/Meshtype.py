#!/usr/bin/env python
# encoding: utf-8

import numpy as np

from OpenGL import GL


__all__ = [
    "Point",
    "Lines",
    "TriangleMesh",
    "QuadMesh",
    "PolygonMesh",
]


class MeshType(object):
    def __init__(self):
        pass

    def init(self):
        pass

    def __call__(self, data):
        GL.glDrawArrays(GL.GL_POINTS, 0, data.shape[0] // 3)


class Point(MeshType):
    pass


class Lines(object):
    def __init__(self, ids=None, data=None):
        if (ids is None) and (data is not None):
            l = len(data.flatten()) // 3
            self._ids = np.array(
                    range(l),
                    dtype=np.uint32,
            )
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
            # check if the data corresponds to the passed shape
            if data.shape[0] != side_x * side_y:
                raise ValueError(
                    "The shape of the triangle mesh data doesn't match sides!"
                )

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
            self._ids = ids.flatten()

    def __call__(self, data):
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._ids),
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
            self._ids = ids.flatten()

    def __call__(self, data):
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glDrawElements(
            GL.GL_QUADS,
            len(self._ids),
            GL.GL_UNSIGNED_INT,
            self._ids
        )


class PolygonMesh(object):
    def __init__(self, ids):
        self._ids = ids

    def __call__(self, data):
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        for indices in self._ids:
            GL.glDrawElements(
                GL.GL_POLYGON,
                len(indices),
                GL.GL_UNSIGNED_INT,
                indices
            )

