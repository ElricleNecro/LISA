#!/usr/bin/env python
# encoding: utf-8

from OpenGL import GL


class ShadersNotLinked(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class ShaderProgram(object):
    def __init__(self):
        self._id = GL.glCreateProgram()
        self._shaders = list()

    @property
    def id(self):
        return self._id

    def addShader(self, val):
        self._shaders.append(val)
        GL.glAttachShader(
            self.id,
            val.id
        )

    def removeShader(self, val):
        self._shaders.remove(val)
        GL.glDetachShader(
            self.id,
            val.id
        )

    def link(self):
        GL.glLinkProgram(self.id)

        # log = GL.gGetProgramiv(
            # self.id,
            # GL.GL_LINK_STATUS
        # )
        # if not log:
        log = GL.glGetShaderInfoLog(self.id)
        if log:
            raise ShadersNotLinked(log)

    def bind(self):
        GL.glUseProgram(self.id)

    def release(self):
        GL.glUseProgram(0)

    def __add__(self, val):
        self.addShader(val)
        return self

    def __iadd__(self, val):
        self.addShader(val)
        return self

    def __radd__(self, val):
        self.addShader(val)
        return self

    def __contains__(self, val):
        return val in self._shaders

    def __sub__(self, val):
        self.removeShader(val)
        return self

    def __isub__(self, val):
        self.removeShader(val)
        return self

    def __del__(self):
        GL.glDeleteProgram(self.id)
