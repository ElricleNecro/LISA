#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o
import LISA.Matrice as m

from LISA.OpenGL import VAO, VBO, FBO, INDEX_BUFFER, VERTEX_BUFFER, Texture, Shaders
from LISA.gui.widget import Application
from LISA.gui.widget import HorizontalSlider
from LISA.gui.widget import Text
from LISA.Matrice import Vector


class HeightMapFBO(object):
    def __init__(self, *args, **kwargs):

        self._w_fbo = 600
        self._h_fbo = 600

#        self._carre = np.array(
#            [0,0,0, 4,0,0, 4,4,0, 0,0,0, 0,4,0, 4,4,0]
#        )

        self._carre_vertices = np.array(
            [0., 1.]
        ).T.astype(np.float32)
        self._carre_index = np.array(
            [0,0,0, 1,0,0, 1,1,0, 0,0,0, 0,1,0, 1,1,0],
            dtype=np.float32
        )

        # self._tex_coord = np.array(
            # [0,0, 1,0, 1,1, 0,0, 0,1, 1,1],
            # dtype=np.float32
        # )

        # self._model_fbo = m.Identity()
        # self._view_fbo = m.LookAt(m.Vector(3, 0, 3), m.Vector(0, 0, 0), m.Vector(0, 3, 0))
        # self._proj_fbo = m.Perspective(50.0, self._w_fbo / self._h_fbo, 1., 100.)

        npoints = 80
        X = np.linspace(-1, 1, npoints).astype(np.float32)
        Y = np.linspace(-1, 1, npoints).astype(np.float32)
        Z = np.zeros((npoints, npoints), dtype=np.float32)
        x, y = np.meshgrid(X, Y)
        self.data = np.vstack((x, y, Z)).reshape(3, -1).T.astype(np.float32)
        self._plot_prop = o.TriangleMesh(
                data=np.vstack((x, y, Z)).reshape(3, -1).T.astype(np.float32),
                side_x=npoints,
                side_y=npoints,
        )
        self._model = m.Identity()

        self.light_position = Vector(0, 1, 10, 1, dtype=np.float32)
        self.light_intensities = Vector(1, 1, 1, dtype=np.float32)
        self.attenuation = Vector(0.01, dtype=np.float32)
        self.ambient = Vector(0.05, dtype=np.float32)
        self.shininess = Vector(0.005, dtype=np.float32)
        self.specularColor = Vector(0.5, 0.5, 0.5, dtype=np.float32)

        self._shaders = Shaders()
        self._shaders += t.shader_path("framebuffer/heightmap.vsh")
        self._shaders += t.shader_path("framebuffer/heightmap.fsh")

        # self._carre_shader = Shaders()
        # self._carre_shader += t.shader_path("framebuffer/framebuffer.vsh")
        # self._carre_shader += t.shader_path("framebuffer/framebuffer.fsh")

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

    def createShader(self, parent):
        self._shaders.build()
        self._shaders.bindAttribLocation("position")

        self._shaders.link()

        # self._carre_shader.build()
        # self._carre_shader.bindAttribLocation("position")
        # self._carre_shader.bindAttribLocation("in_TexCoord0")
        # self._carre_shader.link()

    def createBuffer(self, parent):
        # create buffers
        self._vertices = VBO(VERTEX_BUFFER)
        self._index = VBO(INDEX_BUFFER)
        self._vao = VAO()
        self._fbo = FBO(self._w_fbo, self._h_fbo)

        self._vertices.create()
        self._index.create()
        self._vao.create()
        self._fbo.create()

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

        ##########################
        # We are now creating everything we need for the plan which will
        # contain our render :
        ######################################################################
        # self._carre_vert = VBO(VERTEX_BUFFER)
        # self._carre_idx = VBO(INDEX_BUFFER)
        # self._carre_vao = VAO()

        # self._carre_vert.create()
        # self._carre_idx.create()
        # self._carre_vao.create()

        # # allocate buffers
        # self._vertices.bind()
        # self._vertices.allocate(
            # self._carre_vertices,
            # len(self._carre_vertices) * 4
        # )
        # self._vertices.release()
        # self._index.bind()
        # self._index.allocate(
            # self._carre_index,
            # len(self._carre_index) * 4
        # )
        # self._index.release()

    def createTexture(self, parent):
        texture = Texture.fromImage(
            t.texture_path("heightmap/two.png"),
        )
        texture.parameters = {
            "TEXTURE_MIN_FILTER": "LINEAR",
            "TEXTURE_MAG_FILTER": "LINEAR",
            "TEXTURE_WRAP_S": "CLAMP_TO_EDGE",
            "TEXTURE_WRAP_T": "CLAMP_TO_EDGE",
        }
        texture.load()
        self._shaders.textures << texture

        self._shaders.textures << self._fbo.colorBuffers[0]

    def createShaders(self, parent):
        self.createBuffer(parent)
        self.createShader(parent)
        self.createTexture(parent)

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

        # self._carre_vao.bind()
        # self._carre_vert.bind()
        # self._carre_shader.enableAttributeArray("position")
        # self._carre_shader.setAttributeBuffer(
            # "position",
            # self._carre_vertices,
            # tuplesize=1,
        # )

        # self._carre_shader.enableAttributeArray("in_TexCoord0")
        # self._carre_shader.setAttributeArray(
            # "in_TexCoord0",
            # self._tex_coord,
        # )
        # self._carre_idx.bind()
        # self._carre_vao.release()

    def _first_pass(self, parent):
        self._fbo.bind()

        GL.glClearColor(0., 0., 0., 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # GL.glViewport(0, 0, self._fbo.width, self._fbo.height)

        self._shaders.bind()

        self._shaders.setUniformValue(
            "projection",
            parent._projection,
            #self._proj_fbo,
        )
        self._shaders.setUniformValue(
            "view",
            # self._view_fbo,
            parent._view,
        )
        self._shaders.setUniformValue(
            "model",
            # self._model_fbo,
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
        self._shaders.setUniformValue(
            "image",
            self._shaders.textures.textures[0],
        )
        self._shaders.textures.activate()

        self._vao.bind()

        GL.glDrawElements( GL.GL_TRIANGLES,
            len(self._plot_prop._ids),
            GL.GL_UNSIGNED_INT,
            None,
        )

        self._vao.release()
        self._shaders.textures.release()
        self._shaders.release()

        self._fbo.release()

    def _second_pass(self, parent):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # GL.glViewport(0, 0, self._fbo.width, self._fbo.height)

        self._shaders.bind()

        self._shaders.setUniformValue(
            "projection",
            parent._projection,
            #self._proj_fbo,
        )
        self._shaders.setUniformValue(
            "view",
            # self._view_fbo,
            parent._view,
        )
        self._shaders.setUniformValue(
            "model",
            # self._model_fbo,
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
        self._shaders.setUniformValue(
            "image",
            self._shaders.textures.textures[1],
        )
        self._shaders.textures.activate()

        self._vao.bind()

        GL.glDrawElements(
            GL.GL_TRIANGLES,
            len(self._plot_prop._ids),
            GL.GL_UNSIGNED_INT,
            None,
        )

        self._vao.release()
        self._shaders.textures.release()
        self._shaders.release()
        # GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        # GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # self._carre_shader.bind()

        # self._carre_shader.setUniformValue(
            # "projection",
            # parent._projection,
        # )
        # self._carre_shader.setUniformValue(
            # "view",
            # parent._view,
        # )
        # self._carre_shader.setUniformValue(
            # "model",
            # self._model,
        # )

        # self._carre_shader.textures.activate()

        # self._carre_vao.bind()

        # GL.glDrawElements(
            # GL.GL_TRIANGLES,
            # len(self._carre_index),
            # GL.GL_UNSIGNED_INT,
            # None,
        # )

        # self._carre_vao.release()

        # self._carre_shader.textures.release()
        # self._carre_shader.release()

    def show(self, parent):

        #GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glEnable(GL.GL_DEPTH_TEST)

        self._first_pass(parent)
        self._second_pass(parent)

        GL.glDisable(GL.GL_DEPTH_TEST)

    def _updateAttenuation(self, value):
        self.attenuation[0] = value

    def _updateShininess(self, value):
        self.shininess[0] = 1 + 99 * value

    def _updateAmbient(self, value):
        self.ambient[0] = value

    def _updateDistance(self, value):
        self.light_position[2] = 1.01 + 99 * value

    @property
    def data(self):
        self._modified_data = True
        return self._data
    @data.setter
    def data(self, val):
        self._modified_data = True
        if len(val.shape) != 1:
            self._data = val.flatten()
        else:
            self._data = val

    @property
    def model(self):
        return self._model
    @model.setter
    def model(self, model):
        self._model = model

    @property
    def shaders(self):
        return self._shaders

    def __lshift__(self, inst):
        self._plot_prop = inst

# vim: set tw=79 :
