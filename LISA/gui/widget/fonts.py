#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import LISA.tools as t
# import numpy as np

from OpenGL import GL
from .widget import Widget
from LISA.OpenGL import Buffer, INDEX_BUFFER, VERTEX_BUFFER
from sdl2.ext.color import Color
from sdl2.ext import FontManager as FM


class Text(Widget):

    def __init__(
        self,
        font="/usr/share/fonts/TTF/FreeSans.ttf",
        font_size=14,
        color=Color(255, 255, 255),
        bg_color=Color(0, 0, 0),
    ):

        # init parent
        super(Text, self).__init__()

        # set a default size
        self._font_size = font_size
        self._font = font
        self._color = color
        self._bg_color = bg_color

        # init the fontmanager
        self.set_manager()

        # textures coordinates
        # self._mesh_texture = np.array(
            # [
                # 0, 0,
                # 0, 1,
                # 1, 1,
                # 1, 0,
            # ],
            # dtype=np.float32,
        # )
        # self._indices_texture = np.array([0, 1, 2, 3], dtype=np.uint32)
        # self._npoints_texture = len(self._indices_texture)

    def set_manager(self):
        self._manager = FM(
            font_path=self.font,
            size=self.font_size,
            color=self.color,
            bg_color=self.bg_color,
        )

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = font_size
        self.set_manager()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font):
        self._font = font
        self.set_manager()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = Color(*color)
        self.set_manager()

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, bg_color):
        self._bg_color = Color(*bg_color)
        self.set_manager()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._surface = self._manager.render(self._text)
        self.width = self._surface.w
        self.height = self._surface.h

    def createShaders(self):

        # set shaders
        self._shaders += t.shader_path("text/text.vsh")
        self._shaders += t.shader_path("text/text.fsh")

        # create buffers
        self._vertices = Buffer(VERTEX_BUFFER)
        self._index = Buffer(INDEX_BUFFER)
        self._vertices.create()
        self._index.create()

        # allocate buffers
        self._vertices.bind()
        self._vertices.allocate(
            self._mesh,
            len(self._mesh) * 4
        )
        self._vertices.release()

        # window
        self._index.bind()
        self._index.allocate(
            self._indices,
            len(self._indices) * 4
        )
        self._index.release()

    def draw(self, parent):

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_BLEND)

        self._shaders.bind()

        self._shaders.setUniformValue(
            "modelview",
            parent._widget_projection * self._model
        )

        self._shaders.setUniformValue(
            "corner",
            self._corner,
        )
        self._shaders.setUniformValue(
            "size",
            self._size,
        )

        self._textures = parent.textures << [
            (
                self._surface,
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
            "texture0",
            self._textures[0],
        )
        self._textures[0].activate()

        self._vertices.bind()
        self._shaders.enableAttributeArray("window")
        self._shaders.setAttributeBuffer(
            "window",
            self._mesh,
        )
        self._vertices.release()
        self._index.bind()
        GL.glDrawElements(
            GL.GL_QUADS,
            self._npoints,
            GL.GL_UNSIGNED_INT,
            None
        )
        self._index.release()

        self._shaders.disableAttributeArray("window")
        self._shaders.release()

    def mouseEvent(self, event):
        pass

# vim: set tw=79 :
