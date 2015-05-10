#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import datetime

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o

from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER
from LISA.Matrice import Vector
from LISA.gui.widget import Button, VerticalLayout
from LISA.gui.widget import Application
from LISA.gui.widget import VerticalSlider, HorizontalSlider
from LISA.gui.widget import Spinner


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

    def createShaders(self, world):

        # create buffers
        self._vertices = VBO(VERTEX_BUFFER)
        self._index = VBO(INDEX_BUFFER)
        self._vao = VAO()

        self._vertices.create()
        self._index.create()
        self._vao.create()

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

        self._shaders.build()
        self._shaders.bindAttribLocation("position")

        self._shaders.link()

        self._vao.bind()

        self._index.bind()
        self._vertices.bind()

        self._shaders.enableAttributeArray("position")
        self._shaders.setAttributeBuffer(
            "position",
            self._data,
        )

        self._vao.release()

    def createWidget(self):
        self._widget = Application(layout="horizontal")
        self._widget.title.text = "Window title"
        self._widget.x = 0
        self._widget.y = 0

        # create vertical layout for buttons
        vlayout = VerticalLayout()
        vlayout.size_hint = 1.

        button1 = Button()
        button1.text.font_size = 20
        button1.text = "Hello world !"
        button1.click.connect(self._echo)
        button1.size_hint_x = None
        # button1.size_hint_y = 0.33
        button1.size_hint_y = None

        vlayout.addWidget(button1)

        button2 = Button()
        button2.text.font_size = 20
        button2.text = "Viva Sponge Bob !"
        button2.click.connect(self._echo)
        button2.size_hint_x = None
        # button2.size_hint_y = 0.33
        button2.size_hint_y = None

        vlayout.addWidget(button2)

        # create a integer spinner
        spinner = Spinner()
        spinner.size_hint = None
        spinner.step = 0.01
        vlayout.addWidget(spinner)

        # create the vertical slider
        slider = VerticalSlider()
        hslider = HorizontalSlider()
        vlayout.addWidget(hslider)

        # add the vertical layout and slider to horizontal layout
        self._widget.addWidget(vlayout)
        self._widget.addWidget(slider)

        return self._widget

    def _echo(self):
        print("clicked")

    def paintEvent(self, event):

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        self._shaders.bind()

        self._shaders.setUniformValue(
            "projection",
            event.world._projection
        )
        self._shaders.setUniformValue(
            "modelview",
            event.world._view * self._model
        )
        dt = datetime.datetime.now() - self._time
        second = float((dt.seconds * 1000000 + dt.microseconds) * 0.000006)
        self._shaders.setUniformValue("time", Vector(second, dtype=np.float32))

        self._vao.bind()

        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._plot_prop._ids),
            GL.GL_UNSIGNED_INT,
            None,
        )

        self._vao.release()

        self._shaders.release()


# vim: set tw=79 :
