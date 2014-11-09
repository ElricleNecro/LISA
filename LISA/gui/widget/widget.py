#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import LISA.tools as t
import LISA.Matrice as m

from OpenGL import GL
from LISA.OpenGL import Buffer, INDEX_BUFFER, VERTEX_BUFFER
from LISA.OpenGL import Shaders
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
        self._indices = np.array([0, 1, 2, 3], dtype=np.uint32)
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
        self._mouse = Vector(0., 0., dtype=np.float32)
        self._mouseOffset = Vector(0., 0., dtype=np.float32)

        # init shaders
        self._shaders = Shaders()

        # the matrix model
        self._model = m.Identity()

        # a list of children object
        self._children = []

    def addWidget(self, widget):
        """
        Add a widget in the list of children and set correctly sizes
        accordingly to the parent.
        """

        self._children.append(widget)

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

        self._shaders += t.shader_path("widget/widget.vsh")
        self._shaders += t.shader_path("widget/widget.fsh")

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
            parent._widget_projection * self._model
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
            GL.GL_QUADS,
            self._npoints,
            GL.GL_UNSIGNED_INT,
            None
        )
        self._index.release()

        self._shaders.disableAttributeArray("window")
        self._shaders.release()

    def mouseEvent(self, event):

        # left button of the mouse pressed
        if event[1]:

            # compute the offset of the mouse cursor relative to the corner
            # of the widget, if not already pressed
            if not self._mousePress:
                self._mouse[0] = event.x
                self._mouse[1] = event.y
                self._mouseOffset = self._mouse - self._corner
            if not self._mousePressBorders:
                self._mouse[0] = event.x
                self._mouse[1] = event.y
                self._sizeOffset = self._size - self._mouse + self._corner

            # check that we are inside or not the border used to resize the
            # widget
            if self._inside_border(event.x, event.y):
                self._mousePressBorders = True
            elif self.inside(event.x, event.y) and not self._mousePressBorders:
                self._mousePress = True

        # the left button is released
        if not event[1]:
            self._mousePress = False
            self._mousePressBorders = False

        if self._mousePressBorders:
            self.width = self._sizeOffset[0] + event.x - self._corner[0]
            self.height = self._sizeOffset[1] + event.y - self._corner[1]
            return True
        if self._mousePress:
            self.x = event.x - self._mouseOffset[0]
            self.y = event.y - self._mouseOffset[1]
            return True

    def keyEvent(self, event):
        pass

    def wheelEvent(self, event):
        pass

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
