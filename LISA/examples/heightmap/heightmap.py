#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o

from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER
from LISA.gui.widget import Application
from LISA.gui.widget import HorizontalSlider
from LISA.gui.widget import Text
from LISA.Matrice import Vector


class HeightMap(o.Base):

    def __init__(self, *args, **kwargs):

        npoints = 80
        X = np.linspace(-1, 1, npoints).astype(np.float32)
        Y = np.linspace(-1, 1, npoints).astype(np.float32)
        Z = np.zeros((npoints, npoints), dtype=np.float32)
        x, y = np.meshgrid(X, Y)
        mesh = np.vstack((x, y, Z)).reshape(3, -1).T.astype(np.float32)

        super(HeightMap, self).__init__(
            mesh,
            linetype=o.TriangleMesh(
                data=mesh,
                side_x=npoints,
                side_y=npoints,
            ),
        )

        self.light_position = Vector(0, 1, 10, 1, dtype=np.float32)
        self.light_intensities = Vector(1, 1, 1, dtype=np.float32)
        self.attenuation = Vector(0.01, dtype=np.float32)
        self.ambient = Vector(0.05, dtype=np.float32)
        self.shininess = Vector(0.005, dtype=np.float32)
        self.specularColor = Vector(0.5, 0.5, 0.5, dtype=np.float32)

        self._shaders += t.shader_path("heightmap/heightmap.vsh")
        self._shaders += t.shader_path("heightmap/heightmap.fsh")

    def createWidget(self):
        self._widget = Application(layout="vertical")
        self._widget.title.text = "Sphere mesh"
        self._widget.x = 300
        self._widget.y = 300

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
            self._plot_prop._ids,
            len(self._plot_prop._ids) * 4
        )
        self._index.release()

        self._textures = parent.textures << [
            (
                t.texture_path("heightmap/two.png"),
                {
                    "parameters": {
                        "TEXTURE_MIN_FILTER": "LINEAR",
                        "TEXTURE_MAG_FILTER": "LINEAR",
                        "TEXTURE_WRAP_S": "CLAMP_TO_EDGE",
                        "TEXTURE_WRAP_T": "CLAMP_TO_EDGE",
                    }
                }
            )
        ]

        self._shaders.build()
        self._shaders.bindAttribLocation("position")

        self._shaders.link()

        # Initialization of the VAO
        self._vao.bind()

        self._vertices.bind()
        self._shaders.enableAttributeArray("position")
        self._shaders.setAttributeBuffer(
            "position",
            self._data,
        )

        self._index.bind()

        self._vao.release()

    def show(self, parent):

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

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
            self._textures[0],
        )
        self._textures[0].activate()

        self._vao.bind()

        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._plot_prop._ids),
            GL.GL_UNSIGNED_INT,
            None,
        )

        self._vao.release()
        self._shaders.release()
        self._textures[0].release()

    def _updateAttenuation(self, value):
        self.attenuation[0] = value

    def _updateShininess(self, value):
        self.shininess[0] = 1 + 99 * value

    def _updateAmbient(self, value):
        self.ambient[0] = value

    def _updateDistance(self, value):
        self.light_position[2] = 1.01 + 99 * value

# vim: set tw=79 :
