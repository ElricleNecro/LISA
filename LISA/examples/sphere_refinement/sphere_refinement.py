#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o

from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER
from LISA.Object.Sphere import IcoSphere
from LISA.gui.widget import Application
from LISA.gui.widget import HorizontalSlider
from LISA.gui.widget import Text
from LISA.Matrice import Vector


class SphereRefinement(o.Base):

    def __init__(self, *args, **kwargs):
        super(SphereRefinement, self).__init__(np.asarray([]))

        self._createSphere()

        self.light_position = Vector(0, 10, 0, 1, dtype=np.float32)
        self.light_intensities = Vector(1, 1, 1, dtype=np.float32)
        self.attenuation = Vector(0.01, dtype=np.float32)
        self.ambient = Vector(0.05, dtype=np.float32)
        self.shininess = Vector(0.005, dtype=np.float32)
        self.specularColor = Vector(0.5, 0.5, 0.5, dtype=np.float32)

        self._shaders += t.shader_path("sphere/sphere.vsh")
        self._shaders += t.shader_path("sphere/sphere.fsh")

    def _createSphere(self, camera=[0, 0, 1]):
        # create the mesh
        self.sphere = IcoSphere([0, 0, 0], camera)
        self.sphere()
        self._data = np.asarray(
            self.sphere.positions,
            dtype="float32"
        ).flatten()
        self._indices = np.asarray(
            self.sphere.triangles,
            dtype="uint32"
        ).flatten()

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
        self._widget = Application(layout="vertical")
        self._widget.title.text = "Sphere mesh"
        self._widget.x = 0
        self._widget.y = 0

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
        self.attenuation_slider.changedSlider.connect(self._updateAttenuation)
        self.shininess_slider.changedSlider.connect(self._updateShininess)
        self.ambient_slider.changedSlider.connect(self._updateAmbient)
        self.distance_slider.changedSlider.connect(self._updateDistance)

        return self._widget

    def _changeRefinement(self):
        # recreate the sphere
        self._createSphere(self.camera)

        # recreate the shaders and buffers
        self.createShaders(None)

    def paintEvent(self, event):

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glEnable(GL.GL_CULL_FACE)

        self.camera = np.dot(event.world.rotate[:3, :3].T, event.world.camera)
        self._changeRefinement()

        self._shaders.bind()

        self._shaders.setUniformValue(
            "projection",
            event.world._projection,
        )
        self._shaders.setUniformValue(
            "view",
            event.world._view,
        )
        self._shaders.setUniformValue(
            "model",
            self._model,
        )
        self._shaders.setUniformValue(
            "camera",
            event.world._camera,
        )
        self._shaders.setUniformValue(
            "rotate",
            event.world._rotate,
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

        self._vao.bind()

        GL.glCullFace(GL.GL_BACK)
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._indices),
            GL.GL_UNSIGNED_INT,
            None,
        )

        self._vao.release()

        self._shaders.release()

        GL.glDisable(GL.GL_CULL_FACE)

    def _updateAttenuation(self, value):
        self.attenuation[0] = value

    def _updateShininess(self, value):
        self.shininess[0] = 1 + 99 * value

    def _updateAmbient(self, value):
        self.ambient[0] = value

    def _updateDistance(self, value):
        self.light_position[1] = 1.01 + 99 * value


# vim: set tw=79 :
