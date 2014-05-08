#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from OpenGL import GL
from LISA import common as c


# dictionary for correspondence between numpy dtypes and OpenGL types
DTYPE_TO_GL = dict(
)
DTYPE_TO_GL["float64"] = GL.GL_DOUBLE
DTYPE_TO_GL["float32"] = GL.GL_FLOAT
DTYPE_TO_GL["int32"] = GL.GL_INT
DTYPE_TO_GL["uint8"] = GL.GL_UNSIGNED_BYTE
DTYPE_TO_GL["int8"] = GL.GL_BYTE
DTYPE_TO_GL["uint16"] = GL.GL_UNSIGNED_SHORT
DTYPE_TO_GL["int16"] = GL.GL_SHORT
DTYPE_TO_GL["uint32"] = GL.GL_UNSIGNED_INT
DTYPE_TO_GL["int32"] = GL.GL_INT


# path for texture
def texture_path(texture):
    return c.os.path.join(
        c.TEXTURE_DIR,
        texture,
    )


# path for shaders
def shader_path(shader):
    return c.os.path.join(
        c.SHADERS_DIR,
        shader,
    )

# vim: set tw=79 :
