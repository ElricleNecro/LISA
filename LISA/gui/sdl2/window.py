#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2 as s

from OpenGL import GL
from .hook import _ipython_way_sdl2
from .events import _SDLInput_logger


__all__ = ["SDLWindow"]


class SDLWindow(object):
    def __init__(
        self,
        title,
        w_pos=(s.SDL_WINDOWPOS_UNDEFINED, s.SDL_WINDOWPOS_UNDEFINED),
        size=(800, 480),
        flags=s.SDL_WINDOW_SHOWN | s.SDL_WINDOW_OPENGL | s.SDL_WINDOW_RESIZABLE
    ):

        # create the window with default size
        self._win = s.SDL_CreateWindow(
            title.encode(),
            w_pos[0], w_pos[1],
            size[0], size[1],
            flags
        )
        self._win_name = title

        s.SDL_GL_SetAttribute(s.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        s.SDL_GL_SetAttribute(s.SDL_GL_CONTEXT_MINOR_VERSION, 1)

        # keep a trace of the identity of the window
        self._id = s.SDL_GetWindowID(self._win)

        # set the opengl context of the window
        self._context = s.SDL_GL_CreateContext(self._win)

        self._x = 0.
        self._y = 30.0

        self._widget = []

        self._screensize = size

        _ipython_way_sdl2.add(self)

    def events(self, ev):
        # Deal with events linked to the window:
        _SDLInput_logger.debug(
            "Inside window %d for event.", id(self._win)
        )

        # the window resized
        if ev._resized and hasattr(self, "resizeGL"):
            s.SDL_SetWindowSize(self._win, *ev._window_size)
            self.resizeGL(*ev._window_size)

        # loop over methods and call them if the associated event occurred
        for key in ev._methods.keys():
            if ev._methods[key][0] and hasattr(self, key):
                getattr(self, key)(ev._methods[key][1])

    def makeCurrent(self):
        s.SDL_GL_MakeCurrent(self._win, self._context)

    def draw(self):
        _SDLInput_logger.debug("Inside window %d for drawing.", id(self._win))
        GL.glMatrixMode(GL.GL_PROJECTION | GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glOrtho(-400, 400, 300, -300, 0, 1)
        GL.glClearColor(0, 0, 0, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glRotatef(10.0, 0.0, 0.0, 1.0)
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glVertex2f(self._x, self._y + 90.0)
        GL.glColor3f(0.0, 1.0, 0.0)
        GL.glVertex2f(self._x + 90.0, self._y - 90.0)
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glVertex2f(self._x - 90.0, self._y - 90.0)
        GL.glEnd()

        self._y += 50
        self._y %= 10

        self.update()

    def update(self):
        s.SDL_GL_SwapWindow(self._win)

    def updateWindow(self):
        s.SDL_UpdateWindowSurface(self._win)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def windowSurface(self):
        try:
            return self._s_win
        except:
            self._s_win = s.SDL_GetWindowSurface(self._win)
            return self._s_win

    @property
    def window(self):
        return self._win

    @property
    def name(self):
        return self._win_name
    @name.setter
    def name(self, val):
        s.SDL_SetWindowTitle(self._win, val.encode())
        self._win_name = val

    def close(self):

        # remove the window in the register of window to display in the
        # event loop
        _ipython_way_sdl2.erase(self)

        # destroy the window with SDL
        s.SDL_DestroyWindow(
            self._win
        )

    def mouseEvent(self, event):

        # loop over children widgets
        for widget in self._widget:

            # if the widget has the method call it
            if hasattr(widget, "mouseEvent"):

                # call the widget to see if he process the event
                if widget.mouseEvent(event):

                    # the widget accepts the event and we don't process it
                    # anymore in tis iteration
                    return True

    def keyEvent(self, event):

        # loop over children widgets
        for widget in self._widget:

            # if the widget has the method call it
            if hasattr(widget, "keyEvent"):

                # call the widget to see if he process the event
                if widget.keyEvent(event):

                    # the widget accepts the event and we don't process it
                    # anymore in tis iteration
                    return True

    def wheelEvent(self, event):

        # loop over children widgets
        for widget in self._widget:

            # if the widget has the method call it
            if hasattr(widget, "wheelEvent"):

                # call the widget to see if he process the event
                if widget.wheelEvent(event):

                    # the widget accepts the event and we don't process it
                    # anymore in tis iteration
                    return True

    def resizeGL(self, w, h):
        pass

# vim: set tw=79 :
