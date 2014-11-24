#!/usr/bin/env python
# encoding: utf-8

from os.path import isfile, splitext
from .Shader import Shader, Extension
from .ShaderProgram import ShaderProgram


__all__ = [
    "Shaders",
]

Type = dict(
    vertex = Extension["vsh"],
    fragment = Extension["fsh"],
)


class Shaders(object):
    def __init__(self):
        self._program = None
        self._modified_shader = False
        self._list_shaders = list()

    def build(self):
        self._program = ShaderProgram()
        for a, t in self._list_shaders:
            self._program += Shader(a, t)
        self._modified_shader = False

    @staticmethod
    def CreateShaderFromFile(filename, stype=None):
        # What is the type of the shader, if not given:
        if stype is None:
            ext = splitext(filename)[1][1:].lower()
            stype = Extension[ext]

        # Read the file:
        with open(filename, "r") as f:
            src = f.read()

        # Give it to the Shader class and return the resulting object:
        return (src, stype)

    @staticmethod
    def getTypeFromSource(src):
        # getting the first non empty line:
        for l in src.split('\n'):
            if l == '':
                continue
            else:
                return Type[l.replace('//', '').strip().split(' ')[0].lower()]

    ############
    # To respect the ShaderProgram interface, and be able to replace it:
    ######################################################################
    def setUniformValue(self, *args, **kwargs):
        self._program.setUniformValue(*args, **kwargs)

    def bindAttribLocation(self, name):
        self._program.bindAttribLocation(name)

    def enableAttributeArray(self, *args, **kwargs):
        self._program.enableAttributeArray(*args, **kwargs)

    def setAttributeArray(self, *args, **kwargs):
        self._program.setAttributeArray(*args, **kwargs)

    def setAttributeBuffer(self, *args, **kwargs):
        self._program.setAttributeBuffer(*args, **kwargs)

    def disableAttributeArray(self, *args, **kwargs):
        self._program.disableAttributeArray(*args, **kwargs)

    def link(self):
        if self._modified_shader or self._program is None:
            self.build()
        self._program.link()

    def bind(self):
        if self._modified_shader or self._program is None:
            self._program.delete()
            self.link()

        self._program.bind()

    def release(self):
        self._program.release()


    ############
    # For user's interface:
    ######################################################################
    def addShader(self, val):
        self._modified_shader = True
        if isfile(val):
            #Read the shader from a file:
            self._list_shaders.append(
                    self.CreateShaderFromFile(val)
            )
        else:
            # Read the first line to get the type:
            stype = self.getTypeFromSource(
                    val
            )
            self._list_shaders.append(
                    (val, stype)
            )

    def removeShader(self, val):
        self._modified_shader = True

        if isfile(val):
            val = self.CreateShaderFromFile(val)
        else:
            val = (val, self.getTypeFromSource(val))

        for i, (v, t) in enumerate(self._list_shaders):
            if v == val[0]:
                del self._list_shaders[i]

    def __len__(self):
        return len(self._list_shaders)

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
        return (val, self.getTypeFromSource(val)) in self._shaders

    def __sub__(self, val):
        self.removeShader(val)
        return self

    def __isub__(self, val):
        self.removeShader(val)
        return self

    def delete(self):
        self._program.delete()
