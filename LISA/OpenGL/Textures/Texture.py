#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from OpenGL import GL
from scipy.misc import imread

from LISA.Matrice import Vector
from LISA.tools import DTYPE_TO_GL, texture_path


class Texture(object):

    def __init__(self, kind="2D"):
        self.id = GL.glGenTextures(1)
        self.kind = kind

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def kind(self):
        return self._kind_name

    @kind.setter
    def kind(self, kind):
        self._kind_name = kind.upper()
        self._kind = getattr(GL, "GL_TEXTURE_" + self._kind_name)
        self._teximage = getattr(GL, "glTexImage" + self._kind_name)

    def bind(self):
        GL.glBindTexture(
            self._kind,
            self.id,
        )

    def setParameter(self, param, value):
        GLvalue = self._getValue(value)
        func = self._getTexParameter(GLvalue)
        func(
            self._kind,
            self._getParameter(param),
            GLvalue,
        )

    def _getTexParameter(self, value):
        func = None
        if isinstance(value, float):
            func = GL.glTexParameterf
        elif isinstance(value, int):
            func = GL.glTexParameteri
        elif isinstance(value, Vector):
            if "float" in value.dtype.name:
                func = GL.glTexParameterfv
            elif "int" in value.dtype.name:
                func = GL.glTexParameteriv
        if not func:
            raise ValueError(
                "The passed value isn't already managed <<{0}>>".format(
                    type(value)
                )
            )
        return func

    def _getParameter(self, param):
        parameter = "GL_" + param.upper()
        if hasattr(GL, parameter):
            return getattr(GL, parameter)
        raise AttributeError(
            "The parameter {0} doesn't exist in OpenGL!".format(parameter)
        )

    def _getValue(self, value):
        if isinstance(value, str):
            parameter = "GL_" + value.upper()
            if hasattr(GL, parameter):
                return getattr(GL, parameter)
            raise AttributeError(
                "The value {0} doesn't exist in OpenGL!".format(parameter)
            )
        return value

    def loadImage(self, image, level=0):
        values = [image.shape[x] for x in range(len(image.shape) - 1)]
        values.append(0)
        values.append(self._getFormat(image.shape[len(image.shape) - 1]))
        values.append(DTYPE_TO_GL[image.dtype.name])
        values.append(image)
        self._teximage(
            self._kind,
            level,
            self._getFormat(image.shape[len(image.shape) - 1]),
            *values
        )

    def _getFormat(self, number):
        if number == 1:
            return GL.GL_RED
        else:
            return getattr(GL, "GL_" + "RGBA"[:number])

    def loadImageFromFile(self, filename, dtype="int8"):
        image = imread(
            texture_path(filename)
        )
        image.astype(dtype)
        self.loadImage(image)

# vim: set tw=79 :
