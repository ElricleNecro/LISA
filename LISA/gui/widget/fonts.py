#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import LISA.tools as t
# import numpy as np

from OpenGL import GL
from .widget import Widget
from LISA.OpenGL import VAO, VBO, INDEX_BUFFER, VERTEX_BUFFER
from sdl2.ext.color import Color
from sdl2.ext import FontManager as FM
from LISA.gui.utils.fonts import getDefaultFont


class Text(Widget):

    def __init__(
        self,
        font=getDefaultFont(),
        font_size=14,
        color=[255, 255, 255],
        bg_color=[0, 0, 0],
    ):

        # init parent
        super(Text, self).__init__()

        # set a default size
        self._font_size = font_size
        self._font = font
        self._color = Color(*color)
        self._bg_color = Color(*bg_color)

        # init the fontmanager
        self.set_manager()

        # initiate the trace of the figure
        self._parent_manager = None

        # and texture
        self._textures = None

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
        self._font_size = int(font_size)
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
        if self._parent_manager is not None:
            if self._textures is not None:
                self._parent_manager.textures.remove(id(self._surface))
            self._surface = self._manager.render(self._text)
            self.minWidth = self._surface.w
            # self.width = self._surface.w
            self.minHeight = self._surface.h
            # self.height = self._surface.h
            self._textures = self._parent_manager.textures << [
                (
                    self._surface,
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

    def createShaders(self, parent):

        # keep a trace of the figure
        self._parent_manager = parent
        self.text = self.text

        # set shaders
        self._shaders += t.shader_path("text/text.vsh")
        self._shaders += t.shader_path("text/text.fsh")

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

        self._shaders.build()
        self._shaders.bindAttribLocation("window")
        self._shaders.link()

        self._vao.bind()

        self._vertices.bind()
        self._shaders.enableAttributeArray("window")
        self._shaders.setAttributeBuffer(
            "window",
            self._mesh,
        )
        self._index.bind()

        self._vao.release()

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

        self._shaders.setUniformValue(
            "texture0",
            self._textures[0],
        )
        self._textures[0].activate()

        self._vao.bind()
        GL.glDrawElements(
            GL.GL_TRIANGLES,
            self._npoints,
            GL.GL_UNSIGNED_INT,
            None
        )

        self._vao.release()
        self._shaders.release()
        self._textures[0].release()

    def mouseEvent(self, event):
        pass

# vim: set tw=79 :
