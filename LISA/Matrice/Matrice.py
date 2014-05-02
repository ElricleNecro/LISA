#!/usr/bin/env python
# encoding: utf-8

import math as m
import numpy as np

from .Vector import Vector


D2R = np.pi / 180.


class Matrix(np.ndarray):

    """An upper class over numpy.ndarray to deal with our module matrices."""

    def __init__(self, *args, **kwargs):
        if len(self.shape) == 2:
            if self.shape[0] != self.shape[1]:
                self._dim_str = str(self.shape[0]) + "x" + str(self.shape[1])
            else:
                self._dim_str = str(self.shape[0])

            if self.dtype == np.float32:
                self._dim_str += "f"
            elif self.dtype == np.float32:
                self._dim_str += "d"
            self._dim_str = "glUniformMatrix" + self._dim_str + "v"
        else:
            raise ValueError("Wrong Matrices shape: " + str(len(self.shape)))

        self[:] = np.zeros_like(self)

    @property
    def dim_str(self):
        if len(self.shape) == 2:
            if self.shape[0] != self.shape[1]:
                self._dim_str = str(self.shape[0]) + "x" + str(self.shape[1])
            else:
                self._dim_str = str(self.shape[0])

            if self.dtype == np.float32:
                self._dim_str += "f"
            elif self.dtype == np.float32:
                self._dim_str += "d"
            self._dim_str = "glUniformMatrix" + self._dim_str + "v"
        else:
            raise ValueError("Wrong Matrices shape: " + str(len(self.shape)))

        return self._dim_str

    def _setUniformValue(self, id, GL_ns):
        GL_ns[self._dim_str](id, 1, GL_ns["GL_TRUE"], self.flatten())

    def setToIdentity(self):
        self[:] = 0.
        self.ravel()[0::self.shape[1]+1] = 1.

    def perspective(self, FoV, ratio, near, far):
        res = self * Perspective(FoV, ratio, near, far)
        self[:] = res[:]

    def lookAt(self, pos, center, up):
        tmp = self * LookAt(pos, center, up)
        res = tmp * Translation(-pos)
        self[:] = res[:]

    def __mul__(self, a):
        res = np.dot(self, a)

        mat = Matrix(res.shape, dtype=res.dtype)
        mat[:, :] = res[:, :]

        return mat

    def __rmul__(self, a):
        res = np.dot(a, self)

        mat = Matrix(res.shape, dtype=res.dtype)
        mat[:, :] = res[:, :]

        return mat

    def __imul__(self, a):
        tmp = self * a
        return tmp


def Identity(shape=(4, 4), dtype=np.float32):
    mat = Matrix(shape, dtype, order='C')
    mat.setToIdentity()
    return mat


def Perspective(FoV, ratio, near, far, dtype=np.float32):
    mat = Matrix((4, 4), dtype, order='C')
    f = 1. / m.tan(FoV/2.0 * np.pi / 180.)
    mat[0, 0] = f / ratio
    mat[1, 1] = f
    mat[2, 2] = (near + far) / (near - far)
    mat[2, 3] = 2. * near * far / (near - far)
    mat[3, 2] = -1.

    return mat


def LookAt(pos: Vector, center: Vector, up: Vector, dtype=np.float32):
    mat = Matrix((4, 4), dtype, order='C')

    regard = center - pos
    normal = regard * up
    n_axe = normal * regard

    normal /= normal.norm()
    n_axe /= n_axe.norm()
    regard /= regard.norm()

    mat[0, :3] = normal
    mat[1, :3] = n_axe
    mat[2, :3] = -regard
    mat[3, 3] = 1.

    return mat


def Translation(pos: Vector, dtype=None):
    if not dtype:
        dtype = pos.dtype
    mat = Identity(dtype=dtype)
    mat[:3, 3] = pos[:]

    return mat


def Quaternion(angle, axe: Vector, dtype=None):
    if not dtype:
        dtype = axe.dtype
    mat = Matrix((4, 4), dtype, order='C')

    axe /= axe.norm()
    angle *= D2R

    mat[0, 0] = axe[0] * axe[0] * (1 - m.cos(angle)) + m.cos(angle)
    mat[0, 1] = axe[0] * axe[1] * (1 - m.cos(angle)) - axe[2] * m.sin(angle)
    mat[0, 2] = axe[0] * axe[2] * (1 - m.cos(angle)) + axe[1] * m.sin(angle)

    mat[1, 0] = axe[0] * axe[1] * (1 - m.cos(angle)) + axe[2] * m.sin(angle)
    mat[1, 1] = axe[1] * axe[1] * (1 - m.cos(angle)) + m.cos(angle)
    mat[1, 2] = axe[1] * axe[2] * (1 - m.cos(angle)) - axe[0] * m.sin(angle)

    mat[2, 0] = axe[0] * axe[2] * (1 - m.cos(angle)) - axe[1] * m.sin(angle)
    mat[2, 1] = axe[1] * axe[2] * (1 - m.cos(angle)) + axe[0] * m.sin(angle)
    mat[2, 2] = axe[2] * axe[2] * (1 - m.cos(angle)) + m.cos(angle)

    mat[3, 3] = 1.0

    return mat
