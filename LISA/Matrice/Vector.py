#!/usr/bin/env python
# encoding: utf-8

import numpy as np


class Vector(np.ndarray):

    """Vector dealing class"""
    def __new__(cls, *args, dtype=np.float32, **kwargs):
        buf = np.array(args, dtype=dtype)
        if len(buf.shape) != 1:
            raise ValueError(
                "This class should only contain vector:" +
                " len(shape) = %d != 1" % (
                    len(buf.shape)
                )
            )
        return super(Vector, cls).__new__(
            cls,
            buf.shape,
            dtype=dtype,
            buffer=buf,
            order='C',
            **kwargs
        )

    def __init__(self, *args, **kwargs):
        self._dim_str = str(self.shape[0])

        if self.dtype == np.float32:
            self._dim_str += "f"
        elif self.dtype == np.float32:
            self._dim_str += "d"
        self._dim_str = "glUniform" + self._dim_str + "v"

    def __mul__(self, a):
        if isinstance(a, Vector):
            return Vector(*np.cross(self, a).tolist())
        return Vector(
            *(
                super(Vector, self).__mul__(a)
            ).tolist()
        )

    def __rmul__(self, a):
        if isinstance(a, Vector):
            return Vector(*np.cross(a, self).tolist())
        return Vector(
            *(
                super(Vector, self).__rmul__(a)
            ).tolist()
        )

    def __imul__(self, a):
        self = self * a

    def __lshift__(self, a):
        return Vector(*np.dot(self, a).tolist())

    def __rlshift(self, a):
        return Vector(*np.dot(self, a).tolist())

    def __ilshift__(self, a):
        self = self << a

    def norm(self):
        return np.linalg.norm(self)

    def normalized(self):
        return Vector(*self.tolist()) / self.norm()
