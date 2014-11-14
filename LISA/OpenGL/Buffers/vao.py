#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from OpenGL import GL

from .Buffer import Buffer


__all__ = [
    "VAO"
]

class VAO(Buffer):
    """
    A class to manage vertex attribute object in OpenGL.
    """

    def create(self):
        """
        Create the buffer object by giving it a name obtain through the OpenGL
        API.
        """

        self._id = GL.glGenVertexArrays(1)

        if self._id == 0:
            raise ValueError("The Vertex Array can't be created!")

    def delete(self):
        GL.glDeleteVertexArrays(1, [ self._id ])

    def bind(self):
        GL.glBindVertexArray(self._id)

    def release(self):
        GL.glBindVertexArray(0)


# vim: set tw=79 :
