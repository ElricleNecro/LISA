#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import LISA.tools as t

from OpenGL import GL
from LISA.OpenGL import Buffer, INDEX_BUFFER, VERTEX_BUFFER
from LISA.OpenGL import Shaders as s
from LISA.Matrice import Vector


class Widget(object):

    def __init__(self):

        # the mesh used to draw the widget on the screen
        self._mesh = np.array(
            [0., 0., 0.0,
             0., 1, 0.0,
             1, 1, 0.0,
             1, 0, 0.0],
            dtype=np.float32,
        )
        self._indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        self._npoints = len(self._indices)

        # the upper left corner of the widget
        self._x, self._y = 0., 0.
        self._corner = Vector(self._x, self._y, dtype=np.float32)

        # the size of the widget
        self._width, self._height = 100., 300.
        self.minWidth, self.minHeight = 40, 60
        self._size = Vector(self._width, self._height, dtype=np.float32)

        # for borders
        self._borders = [10, 10]

        # for events
        self._mousePress = False
        self._mousePressBorders = False

    @property
    def minWidth(self):
        return self._minWidth

    @minWidth.setter
    def minWidth(self, minWidth):
        self._minWidth = minWidth

    @property
    def minHeight(self):
        return self._minHeight

    @minHeight.setter
    def minHeight(self, minHeight):
        self._minHeight = minHeight

    @property
    def x_border(self):
        return self._x_border

    @x_border.setter
    def x_border(self, x_border):
        self._x_border = x_border
        self._border[0] = self._x_border

    @property
    def y_border(self):
        return self._y_border

    @y_border.setter
    def y_border(self, y_border):
        self._y_border = y_border
        self._border[1] = self._y_border

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        if self._width <= self.minWidth:
            self._width = self.minWidth
        self._size[0] = self._width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        if self._height <= self.minHeight:
            self._height = self.minHeight
        self._size[1] = self._height

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self._corner[0] = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self._corner[1] = self._y

    def createShaders(self):

        self._shaders = s.CreateShaderFromFile(
            t.shader_path("widget/widget.vsh")
        ) + s.CreateShaderFromFile(
            t.shader_path("widget/widget.fsh")
        )

        self._shaders.link()

        # create buffers
        self._vertices = Buffer(VERTEX_BUFFER)
        self._index = Buffer(INDEX_BUFFER)
        self._vertices.create()
        self._index.create()

        # allocate buffers
        self._vertices.bind()
        self._vertices.allocate(
            self._mesh,
            len(self._mesh) * 4
        )
        self._vertices.release()
        self._index.bind()
        self._index.allocate(
            self._indices,
            len(self._indices) * 4
        )
        self._index.release()

    def draw(self, parent):

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_BLEND)

        self._shaders.bind()

        self._shaders.setUniformValue(
            "modelview",
            parent._widget_projection * parent._model
        )

        self._shaders.setUniformValue(
            "corner",
            self._corner,
        )
        self._shaders.setUniformValue(
            "size",
            self._size,
        )

        self._vertices.bind()
        self._shaders.enableAttributeArray("window")
        self._shaders.setAttributeBuffer(
            "window",
            self._mesh,
        )
        self._vertices.release()

        self._index.bind()
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            self._npoints,
            GL.GL_UNSIGNED_INT,
            None
        )
        self._index.release()

        self._shaders.disableAttributeArray("window")
        self._shaders.release()

    def mousePressEvent(self, event):
        if self._inside_border(event._x, event._y):
            self._mousePressBorders = True
        else:
            self._mousePress = True

    def mouseMoveEvent(self, event):
        if self._mousePress:
            # compute the movement of the mouse
            self.x += event._xRel
            self.y += event._yRel

        if self._mousePressBorders:
            self.width += event._xRel
            self.height += event._yRel

    def mouseReleaseEvent(self, event):
        self._mousePress = False
        self._mousePressBorders = False

    def inside(self, x, y):
        """
        Method returning true if the widget accepts the events because the
        mouse is over it, else returns false.
        """
        return (
            self._corner[0] <= x <= self._corner[0] + self._size[0]
            and
            self._corner[1] <= y <= self._corner[1] + self._size[1]
        )

    def _inside_border(self, x, y):
        return (
            self._corner[0] + self._size[0] - self._borders[0] <=
            x <= self._corner[0] + self._size[0]
            and
            self._corner[1] + self._size[1] - self._borders[1] <=
            y <= self._corner[1] + self._size[1]
        )

# vim: set tw=79 :
