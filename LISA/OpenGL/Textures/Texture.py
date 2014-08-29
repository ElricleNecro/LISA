#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from OpenGL import GL
from scipy.misc import imread

from LISA.Matrice import Vector
from LISA.tools import DTYPE_TO_GL, texture_path


__all__ = ["Texture", "TextureLinear"]


class Texture(object):

    def __init__(self, kind="2D", parameters={}):
        self.id = GL.glGenTextures(1)
        self.kind = kind
        self._binded = False
        self.parameters = parameters
        self.unit = 0

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

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = parameters
        for key, value in self._parameters.items():
            self.setParameter(key, value)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit

    def bind(self):
        if not self._binded:
            GL.glBindTexture(
                self._kind,
                self.id,
            )
            self._binded = True

    def release(self):
        """
        To indicate that the texture should not be used anymore.
        """
        self._binded = False

    def setParameter(self, param, value):
        GLvalue = self._getValue(value)
        func = self._getTexParameter(GLvalue)
        self.bind()
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
        self.bind()
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

    def activate(self):
        GL.glActiveTexture(GL.GL_TEXTURE0 + self.unit)
        self.bind()

    def _setUniformValue(self, location, GL_ns):
        GL_ns["glUniform1i"](location, self.unit)

    def __del__(self):
        GL.glDeleteTextures(1, self.id)


class TextureLinear(Texture):
    """
    A simple texture class for image to apply on a surface.
    """

    def __init__(self):
        super(TextureLinear, self).__init__(
            parameters={
                "TEXTURE_MIN_FILTER": "LINEAR",
                "TEXTURE_MAG_FILTER": "LINEAR",
                "TEXTURE_WRAP_S": "CLAMP",
                "TEXTURE_WRAP_T": "CLAMP",
            }
        )
# vim: set tw=79 :
