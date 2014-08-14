#!/usr/bin/env python
# encoding: utf-8

import os
from OpenGL import GL
from . import ShaderProgram as s
from .exceptions import ShaderCompileError


VERTEX_SHADER = GL.GL_VERTEX_SHADER
FRAGMENT_SHADER = GL.GL_FRAGMENT_SHADER


Extension = dict(
    fsh=FRAGMENT_SHADER,
    vsh=VERTEX_SHADER,
)


class Shader(object):
    def __init__(self, src, stype):
        self.id = stype
        self.src = src

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, val):
        self._src = val
        GL.glShaderSource(
            self.id,
            val
        )
        GL.glCompileShader(self.id)
        log = GL.glGetShaderInfoLog(self.id)
        if log:
            raise ShaderCompileError(log)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = GL.glCreateShader(
            val
        )

    def _addShader(self, val):
        if isinstance(val, s.ShaderProgram):
            return val + self
        sp = s.ShaderProgram()
        sp += self
        sp += val
        return sp

    def __add__(self, val):
        return self._addShader(val)

    def __radd__(self, val):
        return self._addShader(val)


def CreateShaderFromFile(filename, stype=None):
    # What is the type of the shader, if not given:
    if stype is None:
        ext = os.path.splitext(filename)[1][1:].lower()
        stype = Extension[ext]

    # Read the file:
    with open(filename, "r") as f:
        src = f.read()

    # Give it to the Shader class and return the resulting object:
    return Shader(src, stype)
