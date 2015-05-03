#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o
import LISA.Matrice as m

from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER, Texture
from LISA.gui.widget import Application
from LISA.gui.widget import HorizontalSlider
from LISA.gui.widget import Text
from LISA.Matrice import Vector


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

        # create normals
        self._normals = np.empty(3*len(X), dtype=np.float32)
        self._normals[::3] = X
        self._normals[1::3] = Y
        self._normals[2::3] = Z

        self.angle = 0.

        self.light_position = Vector(0, 10, 0, 1, dtype=np.float32)
        self.light_intensities = Vector(1, 1, 1, dtype=np.float32)
        self.attenuation = Vector(0.01, dtype=np.float32)
        self.ambient = Vector(0.05, dtype=np.float32)
        self.shininess = Vector(0.005, dtype=np.float32)
        self.specularColor = Vector(0.5, 0.5, 0.5, dtype=np.float32)

        self._shaders += t.shader_path("earth_lighting/earth_lighting.vsh")
        self._shaders += t.shader_path("earth_lighting/earth_lighting.fsh")

    def createShaders(self, parent):

        # create buffers
        self._vertices = VBO(VERTEX_BUFFER)
        self._index = VBO(INDEX_BUFFER)
        self._nvertices = VBO(VERTEX_BUFFER)
        self._nindex = VBO(INDEX_BUFFER)
        self._vao = VAO()

        self._vertices.create()
        self._index.create()
        self._nvertices.create()
        self._nindex.create()
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
        self._nvertices.bind()
        self._nvertices.allocate(
            self._normals,
            len(self._normals) * 4
        )
        self._nvertices.release()
        self._nindex.bind()
        self._nindex.allocate(
            self._plot_prop._ids,
            len(self._plot_prop._ids) * 4
        )
        self._nindex.release()

        texture = Texture.fromImage(t.texture_path("earth/earth.jpg"))
        texture.parameters = {
            "TEXTURE_MIN_FILTER": "LINEAR",
            "TEXTURE_MAG_FILTER": "LINEAR",
            "TEXTURE_WRAP_S": "CLAMP_TO_EDGE",
            "TEXTURE_WRAP_T": "CLAMP_TO_EDGE",
        }
        texture.format = "RGB"
        texture.load()
        self._shaders.textures << texture

        self._shaders.build()
        self._shaders.bindAttribLocation("position")
        self._shaders.bindAttribLocation("normal")
        self._shaders.link()

        self._vao.bind()

        self._vertices.bind()
        self._shaders.enableAttributeArray("position")
        self._shaders.setAttributeBuffer(
            "position",
            self._data,
        )
        self._index.bind()

        self._nvertices.bind()
        self._shaders.enableAttributeArray("normal")
        self._shaders.setAttributeBuffer(
            "normal",
            self._normals,
        )
        self._nindex.bind()

        self._vao.release()

    def createWidget(self):
        self._widget = Application(layout="vertical")
        self._widget.title.text = "Earth mover"
        self._widget.x = 0
        self._widget.y = 0

        # create the slider
        self.rotation_text = Text()
        self.rotation_text.text = "Rotation speed"
        self._widget.addWidget(self.rotation_text)
        self.rotation_slider = HorizontalSlider()
        self._widget.addWidget(self.rotation_slider)

        # create a slider for attenuation
        self.attenuation_text = Text()
        self.attenuation_text.text = "Attenuation"
        self._widget.addWidget(self.attenuation_text)
        self.attenuation_slider = HorizontalSlider()
        self._widget.addWidget(self.attenuation_slider)

        # create a slider for shininess
        self.shininess_text = Text()
        self.shininess_text.text = "Shininess"
        self._widget.addWidget(self.shininess_text)
        self.shininess_slider = HorizontalSlider()
        self._widget.addWidget(self.shininess_slider)

        # create a slider for ambient
        self.ambient_text = Text()
        self.ambient_text.text = "Ambient"
        self._widget.addWidget(self.ambient_text)
        self.ambient_slider = HorizontalSlider()
        self._widget.addWidget(self.ambient_slider)

        # create a slider for distance
        self.distance_text = Text()
        self.distance_text.text = "Light distance"
        self._widget.addWidget(self.distance_text)
        self.distance_slider = HorizontalSlider()
        self._widget.addWidget(self.distance_slider)

        # connect the slider to the rotation of the earth
        self.rotation_slider.changedSlider.connect(self._updateModel)
        self.attenuation_slider.changedSlider.connect(self._updateAttenuation)
        self.shininess_slider.changedSlider.connect(self._updateShininess)
        self.ambient_slider.changedSlider.connect(self._updateAmbient)
        self.distance_slider.changedSlider.connect(self._updateDistance)

        return self._widget

    def _updateModel(self, value):
        """
        The value of the slider is between 0 and 1, so rescale to allow a
        rotation of the model from one side to an other one.
        """

        self.angle = (value - 0.5) * 3.14159

    def _updateAttenuation(self, value):
        self.attenuation[0] = value

    def _updateShininess(self, value):
        self.shininess[0] = 1 + 99 * value

    def _updateAmbient(self, value):
        self.ambient[0] = value

    def _updateDistance(self, value):
        self.light_position[1] = 1.01 + 99 * value

    def show(self, parent):

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
            parent._projection,
        )
        self._shaders.setUniformValue(
            "view",
            parent._view,
        )
        self._shaders.setUniformValue(
            "model",
            self._model,
        )
        self._shaders.setUniformValue(
            "camera",
            parent._camera,
        )
        self._shaders.setUniformValue(
            "rotate",
            parent._rotate,
        )
        self._shaders.setUniformValue(
            "light.position",
            self.light_position,
        )
        self._shaders.setUniformValue(
            "light.intensities",
            self.light_intensities,
        )
        self._shaders.setUniformValue(
            "light.attenuation",
            self.attenuation,
        )
        self._shaders.setUniformValue(
            "light.ambientCoefficient",
            self.ambient,
        )
        self._shaders.setUniformValue(
            "materialShininess",
            self.shininess,
        )
        self._shaders.setUniformValue(
            "materialSpecularColor",
            self.specularColor,
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

        self._vao.release()

        self._shaders.textures.release()
        self._shaders.release()

        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glDisable(GL.GL_BLEND)


# vim: set tw=79 :
