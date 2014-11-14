#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o

from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER


class HeightMap(o.Base):

    def __init__(self, *args, **kwargs):

        npoints = 80
        X = np.linspace(-1, 1, npoints).astype(np.float32)
        Y = np.linspace(-1, 1, npoints).astype(np.float32)
        Z = np.zeros((npoints,npoints), dtype=np.float32)
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

        self._shaders += t.shader_path("heightmap/heightmap.vsh")
        self._shaders += t.shader_path("heightmap/heightmap.fsh")

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

        # Initialization of the VAO
        self._shaders.bind()
        self._vao.bind()

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

        self._vao.release()
        self._shaders.release()

    def show(self, parent):

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        self._shaders.bind()
        self._vao.bind()

        self._shaders.setUniformValue(
            "projection",
            parent._projection
        )
        self._shaders.setUniformValue(
            "modelview",
            parent._view * self._model
        )

        self._textures = parent.textures << [
            (
                "heightmap/two.png",
                {
                    "parameters": {
                        "TEXTURE_MIN_FILTER": "LINEAR",
                        "TEXTURE_MAG_FILTER": "LINEAR",
                        "TEXTURE_WRAP_S": "CLAMP",
                        "TEXTURE_WRAP_T": "CLAMP",
                    }
                }
            )
        ]

        self._shaders.setUniformValue(
            "map",
            self._textures[0],
        )
        self._textures[0].activate()

        # self._vertices.bind()
        # self._shaders.enableAttributeArray("position")
        # self._shaders.setAttributeBuffer(
            # "position",
            # self._data,
        # )
        # self._vertices.release()

        # self._index.bind()

        # GL.glDrawElements(
            # GL.GL_TRIANGLES,
            # len(self._plot_prop._ids),
            # GL.GL_UNSIGNED_INT,
            # None,
        # )

        # self._index.release()

        # self._shaders.disableAttributeArray("position")
        GL. glDrawArrays(GL.GL_TRIANGLES, 0, self._data.shape[0]//3)

        self._vao.release()
        self._shaders.release()

# vim: set tw=79 :
