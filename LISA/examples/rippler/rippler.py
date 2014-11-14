#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import datetime

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o

from LISA.OpenGL import Buffer, INDEX_BUFFER, VERTEX_BUFFER
from LISA.Matrice import Vector
from LISA.gui.widget import Button, VerticalLayout, HorizontalLayout


class Rippler(o.Base):

    def __init__(self, *args, **kwargs):

        npoints = 30
        X = np.linspace(-1, 1, npoints).astype(np.float32)
        Y = np.linspace(-1, 1, npoints).astype(np.float32)
        Z = np.zeros((npoints, npoints), dtype=np.float32)
        x, y = np.meshgrid(X, Y)
        mesh = np.vstack((x, y, Z)).reshape(3, -1).T.astype(np.float32)

        super(Rippler, self).__init__(mesh, linetype=o.TriangleMesh(data=mesh))

        self._shaders += t.shader_path("rippler/rippler.vsh")
        self._shaders += t.shader_path("rippler/rippler.fsh")

        self._time = datetime.datetime.now()

        # self._widget = HorizontalLayout()
        self._widget = VerticalLayout()
        button1 = Button(font_size=20)
        button2 = Button(font_size=20)
        button1.text = "Hello world !"
        button2.text = "Viva Sponge Bob !"
        self._widget.x = 300
        self._widget.y = 300
        button1.click.connect(self._echo)
        button2.click.connect(self._echo)
        # button1.size_hint_x = 0.3
        # button2.size_hint_x = 0.7
        button1.size_hint_y = 0.5
        button2.size_hint_y = 0.5
        self._widget.addWidget(button1)
        self._widget.addWidget(button2)

    def createShaders(self, parent):

        # create buffers
        self._vertices = Buffer(VERTEX_BUFFER)
        self._index = Buffer(INDEX_BUFFER)
        self._vertices.create()
        self._index.create()

        # allocate buffers
        self._vertices.bind()
        self._vertices.allocate(
            self._data,
            len(self._data) * 4
        )
        self._vertices.release()
        self._index.bind()
        self._index.allocate(
            self._plot_prop._ids,
            len(self._plot_prop._ids) * 4
        )
        self._index.release()

        # create shaders for widget
        self._widget.createShaders()

    def createWidget(self):

        return self._widget

    def _echo(self):
        print("clicked")

    def show(self, parent):

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        self._shaders.bind()

        self._shaders.setUniformValue(
            "projection",
            parent._projection
        )
        self._shaders.setUniformValue(
            "modelview",
            parent._view * self._model
        )
        dt = datetime.datetime.now() - self._time
        second = float((dt.seconds * 1000000 + dt.microseconds) * 0.000006)
        self._shaders.setUniformValue("time", Vector(second, dtype=np.float32))

        self._vertices.bind()
        self._shaders.enableAttributeArray("position")
        self._shaders.setAttributeBuffer(
            "position",
            self._data,
        )
        self._vertices.release()

        self._index.bind()

        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._plot_prop._ids),
            GL.GL_UNSIGNED_INT,
            None,
        )

        self._index.release()

        self._shaders.disableAttributeArray("position")
        self._shaders.release()

# vim: set tw=79 :
