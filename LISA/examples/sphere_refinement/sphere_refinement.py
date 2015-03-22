#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o

from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER
from LISA.Object.Sphere import IcoSphere
from LISA.gui.widget import Application
from LISA.gui.widget import Spinner
from LISA.gui.widget import Text


class SphereRefinement(o.Base):

    def __init__(self, *args, **kwargs):
        super(SphereRefinement, self).__init__(np.asarray([]))

        self._createSphere(3)

        self._shaders += t.shader_path("basic.vsh")
        self._shaders += t.shader_path("basic.fsh")

    def _createSphere(self, level):
        # create the mesh
        self.sphere = IcoSphere()
        self.sphere(level)
        self._data = np.asarray(
            self.sphere.positions,
            dtype="float32"
        ).flatten()
        self._indices = np.asarray(
            self.sphere.triangles,
            dtype="uint32"
        ).flatten()

    def createShaders(self, parent):

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
            self._indices,
            len(self._indices) * 4
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
        self._widget.title.text = "Sphere with refinement"
        self._widget.x = 300
        self._widget.y = 300

        # create a text label
        self.label = Text()
        self.label.text = "Level of refinement"
        self._widget.addWidget(self.label)

        # create a integer spinner
        self.spinner = Spinner()
        self.spinner.size_hint = None
        self.spinner.step = 1
        self.spinner.currentValue = 3
        self._widget.addWidget(self.spinner)

        # connect to the changed value signal
        self.spinner.changedCurrentValue.connect(self._changeRefinement)

        return self._widget

    def _changeRefinement(self, value):
        # check bounds
        if value < 0:
            return

        # recreate the sphere
        self._createSphere(value)

        # recreate the shaders and buffers
        self.createShaders(None)

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

        self._vao.bind()

        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._indices),
            GL.GL_UNSIGNED_INT,
            None,
        )

        self._vao.release()

        self._shaders.release()

# vim: set tw=79 :
