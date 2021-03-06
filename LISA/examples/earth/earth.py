#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from OpenGL import GL

import LISA.tools as t
import LISA.Object as o

from LISA.OpenGL import Buffer, INDEX_BUFFER, VERTEX_BUFFER


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

        self._shaders += t.shader_path("earth/earth.vsh")
        self._shaders += t.shader_path("earth/earth.fsh")

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

    def show(self, parent):

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_BLEND)

        self._shaders.bind()

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
                "earth/earth2.png",
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

        self._vertices.bind()
        self._shaders.enableAttributeArray("position")
        self._shaders.setAttributeBuffer(
            "position",
            self._data,
        )
        self._vertices.release()

        self._index.bind()

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

        self._index.release()

        self._shaders.disableAttributeArray("position")
        self._shaders.release()
        self._textures[0].release()

        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glDisable(GL.GL_BLEND)

# vim: set tw=79 :
