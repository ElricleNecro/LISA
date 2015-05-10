#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o
import LISA.Matrice as m

from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER, Texture
from LISA.gui.widget import HorizontalLayout
from LISA.gui.widget import Application
from LISA.gui.widget import HorizontalSlider


class Earth(o.Base):

    def __init__(self, *args, **kwargs):

        npoints = 800
        phi = np.linspace(0, 2. * np.pi, npoints).astype(np.float32)
        theta = np.linspace(
            0.5 * np.pi,
            -0.5 * np.pi,
            npoints,
        ).astype(np.float32)
        r = np.zeros((npoints, npoints), dtype=np.float32)
        r[:, :] = 1.
        p, tt = np.meshgrid(phi, theta)
        mesh = np.vstack((p, tt, r)).reshape(3, -1).T.astype(np.float32)

        super(Earth, self).__init__(
            mesh,
            linetype=o.TriangleMesh(
                data=mesh,
                side_x=npoints,
                side_y=npoints,
            ),
        )

        phi = self._data[::3]
        theta = self._data[1::3]
        r = self._data[2::3]
        X = r * np.cos(phi) * np.cos(theta)
        Y = r * np.sin(phi) * np.cos(theta)
        Z = r * np.sin(theta)
        self._data[::3] = X
        self._data[1::3] = Y
        self._data[2::3] = Z

        self.angle = 0.

        self._shaders += t.shader_path("earth/earth.vsh")
        self._shaders += t.shader_path("earth/earth.fsh")

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

        texture = Texture.fromImage(t.texture_path("earth/earth2.png"))
        texture.parameters = {
            "TEXTURE_MIN_FILTER": "LINEAR",
            "TEXTURE_MAG_FILTER": "LINEAR",
            "TEXTURE_WRAP_S": "CLAMP_TO_EDGE",
            "TEXTURE_WRAP_T": "CLAMP_TO_EDGE",
        }
        texture.load()
        self._shaders.textures << texture

        self._shaders.build()
        self._shaders.bindAttribLocation("position")
        self._shaders.link()

        self._vao.bind()

        self._vertices.bind()
        self._shaders.enableAttributeArray("position")
        self._shaders.setAttributeBuffer(
            "position",
            self._data,
        )
        self._index.bind()

        self._vao.release()

    def createWidget(self):
        self._widget = Application(layout="vertical")
        self._widget.title.text = "Earth mover"
        self._widget.x = 0
        self._widget.y = 0

        # create vertical layout for buttons
        hlayout = HorizontalLayout()
        hlayout.size_hint = 1.

        # create the slider
        hslider = HorizontalSlider()
        hlayout.addWidget(hslider)

        # connect the slider to the rotation of the earth
        hslider.changedSlider.connect(self._updateModel)

        # add the vertical layout and slider to horizontal layout
        self._widget.addWidget(hlayout)

        return self._widget

    def _updateModel(self, value):
        """
        The value of the slider is between 0 and 1, so rescale to allow a
        rotation of the model from one side to an other one.
        """

        self.angle = (value - 0.5) * 3.14159

    def paintEvent(self, event):

        # rotate against z axis
        self.model *= m.Quaternion(self.angle, m.Vector(0., 0., 1.))

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_BLEND)

        self._shaders.bind()

        self._shaders.setUniformValue(
            "projection",
            event.world._projection
        )
        self._shaders.setUniformValue(
            "modelview",
            event.world._view * self._model
        )

        self._shaders.setUniformValue(
            "map",
            self._shaders.textures.textures[0],
        )
        self._shaders.textures.activate()

        self._vao.bind()
        GL.glCullFace(GL.GL_FRONT)
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._plot_prop._ids),
            GL.GL_UNSIGNED_INT,
            None,
        )
        GL.glCullFace(GL.GL_BACK)
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._plot_prop._ids),
            GL.GL_UNSIGNED_INT,
            None,
        )

        self._vao.release()

        self._shaders.textures.release()
        self._shaders.release()

        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glDisable(GL.GL_BLEND)


# vim: set tw=79 :
