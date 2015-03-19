#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes

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
        if self._binded:
            GL.glBindTexture(
                self._kind,
                0,
            )
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
        # hack for cases where we have a one channel texture, can't find
        # something smart at this time
        if len(image.shape) == 2:
            shape = list(image.shape)
            shape += [1]
        else:
            shape = image.shape

        # generate the width, height, deep for all cases of textures
        values = [shape[x] for x in range(len(shape) - 1)]

        # the value that they said to put at zero
        values.append(0)

        # format of the data
        values.append(self._getFormat(shape[len(shape) - 1]))

        # convert image type to opengl type
        values.append(DTYPE_TO_GL[image.dtype.name])

        # add the image
        values.append(image)

        # swap values since the width is expected before the height and numpy
        # array is in the reverse order
        values[0], values[1] = values[1], values[0]

        # bind the texture to the opengl context
        self.bind()

        # say opengl where is the data for the texture
        self._teximage(
            self._kind,
            level,
            self._getFormat(shape[len(shape) - 1]),
            *values
        )

    def _getFormat(self, number):
        if number == 1:
            return GL.GL_RED
        else:
            return getattr(GL, "GL_" + "RGBA"[:number])

    def loadFromSDLSurface(self, surface):
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGBA,
            surface.w,
            surface.h,
            0,
            GL.GL_RGBA,
            GL.GL_UNSIGNED_BYTE,
            ctypes.c_void_p(surface.pixels),
        )

    def loadImageFromFile(self, filename, dtype="uint8"):
        image = imread(filename)
        image = image.astype(dtype)
        self.loadImage(image)

    def activate(self):
        GL.glActiveTexture(GL.GL_TEXTURE0 + self.unit)
        self.bind()

    def _setUniformValue(self, location, GL_ns):
        GL_ns["glUniform1i"](location, self.unit)

    def delete(self):
        GL.glDeleteTextures([self.id])


class TextureLinear(Texture):
    """
    A simple texture class for image to apply on a surface.
    """

    def __init__(self):
        super(TextureLinear, self).__init__(
            parameters={
                "TEXTURE_MIN_FILTER": "LINEAR",
                "TEXTURE_MAG_FILTER": "LINEAR",
                "TEXTURE_WRAP_S": "CLAMP_TO_EDGE",
                "TEXTURE_WRAP_T": "CLAMP_TO_EDGE",
            }
        )
# vim: set tw=79 :
