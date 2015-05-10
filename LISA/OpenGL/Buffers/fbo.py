#!/usr/bin/env python
# encoding: utf-8

from OpenGL import GL

from .Buffer import Buffer
from ..Textures import Texture

__all__ = [
    "FBO",
]


class RenderBuffer(Buffer):
    """Render Buffer, used to deal with depth/stencil buffer (stencil doesn't
    exist anymore in OGL 3).
    """
    def __init__(self):
        self._id = 0

    def create(self):
        self.delete()
        self._id = GL.glGenRenderbuffers(1)

    def bind(self):
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, self._id)

    def release(self):
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, 0)

    def delete(self):
        if GL.glIsRenderbuffer(self._id) == GL.GL_TRUE:
            GL.glDeleteRenderbuffers(1, [self._id])

    def allocate(self, w, h, internalFormat=GL.GL_DEPTH24_STENCIL8):
        GL.glRenderbufferStorage(GL.GL_RENDERBUFFER, internalFormat, w, h)

    @property
    def id(self):
        return self._id


class FBO(Buffer):
    """The Frame Buffer object class.
    """
    def __init__(self, width=480, height=192, textureFormat="RGBA", useStencil=False):
        self._id = 0

        self._width = width
        self._height = height

        self._format = textureFormat

        if not useStencil:
            self._depthFormat = GL.GL_DEPTH_COMPONENT24
        else:
            self._depthFormat = GL.GL_DEPTH24_STENCIL8

        self._useStencil = useStencil

        self._colorBuffers = list()

        self._renderBuffer = RenderBuffer()

    def create(self, nbColorBuffer=1):
        """ Create the frame buffer object, including all the needed color buffer and depth buffer.

        :param nbColorBuffer: Number of color buffer to create.
        :type nbColorBuffer: int
        :raises: ValueError
        """
        if GL.glIsFramebuffer(self._id) == GL.GL_TRUE:
            self.delete()

        self._id = GL.glGenFramebuffers(1)

        self.bind()

        self.loadColorBuffers(nbColorBuffer)
        self.loadRenderBuffer(self._depthFormat)
        for i, tex in enumerate(self._colorBuffers):
            tex.activate()
            GL.glFramebufferTexture2D(
                GL.GL_FRAMEBUFFER,
                getattr(GL, "GL_COLOR_ATTACHMENT" + str(i)),
                GL.GL_TEXTURE_2D,
                tex.id,
                0
            )
            tex.release()

        if not self._useStencil:
            GL.glFramebufferRenderbuffer(
                GL.GL_FRAMEBUFFER,
                GL.GL_DEPTH_ATTACHMENT,
                GL.GL_RENDERBUFFER,
                self._renderBuffer.id
            )
        else:
            GL.glFramebufferRenderbuffer(
                GL.GL_FRAMEBUFFER,
                GL.GL_DEPTH_STENCIL_ATTACHMENT,
                GL.GL_RENDERBUFFER,
                self._renderBuffer.id
            )

        if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
            self.delete()

            raise RuntimeError("Problem with framebuffer instance '%s': creation failed.")

        self.release()

    def bind(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._id)

    def release(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

    def delete(self):
        if GL.glIsFramebuffer(self._id) == GL.GL_TRUE:
            GL.glDeleteFramebuffers(1, [self._id])
        self._renderBuffer.delete()
        self.deleteColorBuffers()

    def loadRenderBuffer(self, internalFormat=GL.GL_DEPTH_COMPONENT24):
        self._renderBuffer.create()
        self._renderBuffer.bind()

        self._renderBuffer.allocate(self._width, self._height, internalFormat)

        self._renderBuffer.release()

    def loadColorBuffers(self, nb=1):
        if nb > 16:
            raise ValueError("A frame buffer can only have 16 color buffer attach to it.")

        for i in range(nb):
            texture = Texture("_fbo_to randomized" + str(nb), width=self._width, height=self._height, format=self._format)
            texture.kind = "2D"
            texture.data = None
            texture.type = GL.GL_UNSIGNED_BYTE
            texture.parameters = {
                "TEXTURE_MIN_FILTER": "LINEAR",
                "TEXTURE_MAG_FILTER": "NEAREST",
            }
            texture.load()
            self._colorBuffers.append(texture)

    def deleteColorBuffers(self):
        for tex in self._colorBuffers:
            tex.delete()

    @property
    def id(self):
        return self._id

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def colorBuffers(self):
        return self._colorBuffers

