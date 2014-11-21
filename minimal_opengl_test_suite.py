#!/usr/bin/env python
# encoding: utf-8

import ctypes
import sdl2 as s
import numpy as np
from OpenGL import GL


class Keyboard(list):
    def __init__(self):
        super(Keyboard, self).__init__(
            [False for i in range(s.SDL_NUM_SCANCODES)]
        )

        self._x, self._y = 0., 0.

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y


class Wheel(object):
    dx = 0.
    dy = 0.


class Mouse(list):
    def __init__(self):
        super(Mouse, self).__init__([False for i in range(8)])

        self._x = 0.
        self._y = 0.

        self._xRel = 0.
        self._yRel = 0.

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val

    @property
    def dx(self):
        return self._xRel

    @dx.setter
    def dx(self, val):
        self._xRel = val

    @property
    def dy(self):
        return self._yRel

    @dy.setter
    def dy(self, val):
        self._yRel = val


class Window(object):
    pass


class SDLInput(object):
    def __init__(self):
        self._mouse = Mouse()
        self._keys = Keyboard()
        self._wheel = Wheel()

        self._end = False

        self._event = s.SDL_Event()
        self._methods = {
            "mouseEvent": [False, self._mouse],
            "keyEvent": [False, self._keys],
            "wheelEvent": [False, self._wheel],
        }

        # window size
        self._window_size = (0., 0.)

    def update(self):

        # say that we don't use any methods in the window
        for key in self._methods.keys():
            self._methods[key][0] = False
        self._resized = False

        # initiialize relative movement to null
        self._mouse.dx, self._mouse.dy = 0., 0.
        self._wheel.dx, self._wheel.dy = 0., 0.

        # loop over event in the queue
        while s.SDL_PollEvent(ctypes.byref(self._event)) != 0:
            # set the id of the window
            self._id = self._event.window.windowID

            if self._event.type == s.SDL_WINDOWEVENT:
                if self._event.window.event == s.SDL_WINDOWEVENT_CLOSE:
                    self._end = True

                elif self._event.window.event == s.SDL_WINDOWEVENT_RESIZED:
                    self._resized = True
                    self._window_size = (
                        self._event.window.data1,
                        self._event.window.data2,
                    )

            elif self._event.type == s.SDL_KEYDOWN:
                self._keys[self._event.key.keysym.scancode] = True

                self._methods["keyEvent"][0] = True

            elif self._event.type == s.SDL_KEYUP:
                self._keys[self._event.key.keysym.scancode] = False

                self._methods["keyEvent"][0] = True

            elif self._event.type == s.SDL_MOUSEBUTTONDOWN:
                self._mouse[self._event.button.button] = True

                self._methods["mouseEvent"][0] = True

            elif self._event.type == s.SDL_MOUSEBUTTONUP:
                self._mouse[self._event.button.button] = False

                self._methods["mouseEvent"][0] = True

            elif self._event.type == s.SDL_MOUSEMOTION:
                self._mouse.dx = self._event.motion.xrel
                self._mouse.dy = self._event.motion.yrel

                self._methods["mouseEvent"][0] = True

            elif self._event.type == s.SDL_MOUSEWHEEL:
                self._wheel.dx = self._event.wheel.x
                self._wheel.dy = self._event.wheel.y

                self._methods["wheelEvent"][0] = True

            else:
                break

        self._mouse.x = self._event.motion.x
        self._mouse.y = self._event.motion.y
        self._keys.x = self._mouse.x
        self._keys.y = self._mouse.y

    @property
    def id(self):
        return self._id

    @property
    def End(self):
        return self._end

    @property
    def keyboard(self):
        return self._keys

    @property
    def mouse(self):
        return self._mouse

    @property
    def wheel(self):
        return self._wheel

    @wheel.setter
    def wheel(self, wheel):
        self._wheel = wheel

    def _showCursor(self, val):
        if type(val) == bool:
            if val:
                s.SDL_ShowCursor(s.SDL_ENABLE)
            else:
                s.SDL_ShowCursor(s.SDL_DISABLE)

    showCursor = property(fset=_showCursor, doc="")



###############
# Creating SDL Window and OpenGL context:
#########################################
s.SDL_Init(s.SDL_INIT_VIDEO)

win = s.SDL_CreateWindow(
    "Test".encode(),
    s.SDL_WINDOWPOS_UNDEFINED, s.SDL_WINDOWPOS_UNDEFINED,
    200, 100,
    s.SDL_WINDOW_SHOWN | s.SDL_WINDOW_OPENGL | s.SDL_WINDOW_RESIZABLE
)

context = s.SDL_GL_CreateContext(win)

s.SDL_GL_SetAttribute(s.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
s.SDL_GL_SetAttribute(s.SDL_GL_CONTEXT_MINOR_VERSION, 3)


###############
# Creting mesh points:
######################
npoints = 80
X = np.linspace(-1, 1, npoints).astype(np.float32)
Y = np.linspace(-1, 1, npoints).astype(np.float32)
Z = np.zeros((npoints,npoints), dtype=np.float32)
x, y = np.meshgrid(X, Y)
mesh = np.vstack((x, y, Z)).reshape(3, -1).T.astype(np.float32).flatten()

###############
# Creating corresponding id's:
##############################
ids = np.empty(
    (npoints - 1, npoints - 1, 6),
    dtype=np.uint32
)
indices = np.array(range(npoints - 1), dtype=np.uint32)
for i in range(npoints - 1):
    ids[:, i, 0] = indices[:] + i * npoints
    ids[:, i, 1] = indices[:] + 1 + i * npoints
    ids[:, i, 2] = indices[:] + (i + 1) * npoints
    ids[:, i, 3] = indices[:] + (i + 1) * npoints
    ids[:, i, 4] = indices[:] + 1 + (i + 1) * npoints
    ids[:, i, 5] = indices[:] + 1 + i * npoints
ids = ids.flatten()


###############
# Creating the associated VBO:
##############################
vbo_id = GL.glGenBuffers(2)

GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_id[0])
vertices = GL.glBufferData(
    GL.GL_ARRAY_BUFFER,
    len(mesh)*4,
    mesh,
    GL.GL_STATIC_DRAW
)
GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vbo_id[1])
vertices = GL.glBufferData(
    GL.GL_ELEMENT_ARRAY_BUFFER,
    len(ids)*4,
    ids,
    GL.GL_STATIC_DRAW
)
GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)


###############
# Creating the shaders:
#######################
sp_id = GL.glCreateProgram()
print(sp_id)

vx_id = GL.glCreateShader(GL.GL_VERTEX_SHADER)
GL.glShaderSource(
    vx_id,
"""
#version 130
#pragma debug(on)

uniform mat4 p;
uniform mat4 m;
in vec3 position;

void main(void)
{
    gl_Position = p * m * vec4(position, 1.0);
}
"""
)
GL.glCompileShader(vx_id)
log = GL.glGetShaderInfoLog(vx_id)
if log:
    raise ValueError(log)

fg_id = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
GL.glShaderSource(
    fg_id,
"""
#version 130
#pragma debug(on)

out vec4 color;

void main()
{
    color = vec4(1.0, 1.0, 1.0, 1.0);
}
"""
)
GL.glCompileShader(fg_id)
log = GL.glGetShaderInfoLog(fg_id)
if log:
    raise ValueError(log)

GL.glAttachShader(sp_id, vx_id)
GL.glAttachShader(sp_id, fg_id)

proj = np.array([[  9.40900505e-01,   0.00000000e+00,   0.00000000e+00,
                  0.00000000e+00],
                 [  0.00000000e+00,   1.73205078e+00,   0.00000000e+00,
                  0.00000000e+00],
                 [  0.00000000e+00,   0.00000000e+00,  -1.00000000e+00,
                  -1.99999999e-06],
                 [  0.00000000e+00,   0.00000000e+00,  -1.00000000e+00,
                  0.00000000e+00]], dtype=np.float32)
perp = np.array([[ 1.,  0.,  0.,  0.],
                 [ 0.,  1.,  0.,  0.],
                 [ 0.,  0.,  1., -1.],
                 [ 0.,  0.,  0.,  1.]], dtype=np.float32)


ev = SDLInput()

GL.glBindAttribLocation(sp_id, 1, "position".encode())

GL.glLinkProgram(sp_id)


###############
# Creating the problematic VAO:
###############################
vao_id = GL.glGenVertexArrays(1)
GL.glBindVertexArray(vao_id)
GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_id[0])
GL.glEnableVertexAttribArray(
    1
)
GL.glVertexAttribPointer(
    1,
    3,
    GL.GL_FLOAT,
    GL.GL_TRUE,
    0,
    None,
)
GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vbo_id[1])
GL.glBindVertexArray(0)



while not ev.End:
    ev.update()

    GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    GL.glUseProgram(sp_id)

    GL.glUniformMatrix4fv(
        GL.glGetUniformLocation(sp_id, "p"),
        1,
        GL.GL_TRUE,
        proj.flatten()
    )
    GL.glUniformMatrix4fv(
        GL.glGetUniformLocation(sp_id, "m"),
        1,
        GL.GL_TRUE,
        perp.flatten()
    )

    # Without VAO:
    # GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_id[0])
    # GL.glEnableVertexAttribArray(
        # 1
    # )
    # GL.glVertexAttribPointer(
        # 1,
        # 3,
        # GL.GL_FLOAT,
        # GL.GL_TRUE,
        # 0,
        # None,
    # )
    # GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    # GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vbo_id[1])
    # GL.glDrawElements(GL.GL_TRIANGLES, len(ids), GL.GL_UNSIGNED_INT, None)
    # GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)

    # GL.glDisableVertexAttribArray(1)

    # With VAO:
    GL.glBindVertexArray(vao_id)
    GL.glDrawElements(GL.GL_TRIANGLES, len(ids), GL.GL_UNSIGNED_INT, None)
    GL.glBindVertexArray(0)

    GL.glUseProgram(0)

    s.SDL_GL_SwapWindow(win)

GL.glDeleteProgram(sp_id)
GL.glDeleteBuffers(2, vbo_id)

s.SDL_DestroyWindow(win)
s.SDL_Quit()
