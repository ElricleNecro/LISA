#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from OpenGL import GL

# type of the buffer
VERTEX_BUFFER = GL.GL_ARRAY_BUFFER
INDEX_BUFFER = GL.GL_ELEMENT_ARRAY_BUFFER

# the usage of the buffer set when allocating
STATIC_DRAW = GL.GL_STATIC_DRAW
STATIC_READ = GL.GL_STATIC_READ
STATIC_COPY = GL.GL_STATIC_COPY
DYNAMIC_DRAW = GL.GL_DYNAMIC_DRAW
DYNAMIC_READ = GL.GL_DYNAMIC_READ
DYNAMIC_COPY = GL.GL_DYNAMIC_COPY
STREAM_DRAW = GL.GL_STREAM_DRAW
STREAM_READ = GL.GL_STREAM_READ
STREAM_COPY = GL.GL_STREAM_COPY


class Buffer(object):
    """
    A class to manage the creation and manipulation of buffer in OpenGL.
    """

    def __init__(self, btype, usage=STATIC_DRAW):
        self.btype = btype
        self.usage = usage

    @property
    def btype(self):
        return self._btype

    @property
    def usage(self):
        return self._usage

    @btype.setter
    def btype(self, btype):
        self._btype = btype

    @usage.setter
    def usage(self, usage):
        self._usage = usage

    def create(self):
        """
        Create the buffer object by giving it a name obtain through the OpenGL
        API.
        """

        self._id = GL.glGenBuffers(1)

        if self._id == 0:
            raise ValueError("The buffer object can't be created!")

    def bind(self):
        GL.glBindBuffer(self._btype, self._id)

    def allocate(self, data, count):
        GL.glBufferData(
            self._btype,
            count,
            data,
            self._usage,
        )

    def release(self):
        GL.glBindBuffer(self._btype, 0)


# vim: set tw=79 :
