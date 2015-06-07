#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2 as s
import logging
import LISA.Matrice as m

from OpenGL import GL
from ..utils.signals import Signal


__all__ = ["SDLWindow"]

logger = logging.getLogger(__name__)


class WindowManager(object):
    """
    A window manager allowing to store and retrieve created windows.
    """
    def __init__(self):
        """
        Init some containers for created windows, and signals.
        """
        # containers
        self.windowsById = {}
        self.windows = []

        # signals
        self.created = Signal()
        self.deleted = Signal()

    def add(self, window):
        """
        Add a window.
        """
        # register the window if properties present
        if hasattr(window, "id"):
            self.windowsById[window.id] = window
        else:
            logger.error(
                "The window {0} must have an id to be "
                "registered".format(window)
            )
        self.windows.append(window)

        # send a signal wiht the created window
        self.created(window)

    def delete(self, window):
        """
        Remove a window from the manager.
        """
        # remove the window in the register of window to display in the
        # event loop
        self.windows.remove(window)
        self.windowsById.pop(window, None)

        # send a signal with the removed window
        self.deleted(window)


class WindowMetaclass(type):
    """
    Metaclass to register created windows and easily get access to them in the
    program according to various properties.
    """

    def __init__(cls, *args, **kwargs):
        """
        Store containers to the class.
        """
        # create the class as usual
        super(WindowMetaclass, cls).__init__(*args, **kwargs)

        # create the container if not present
        if not hasattr(cls, "manager"):
            cls.manager = WindowManager()

    def __call__(cls, *args, **kwargs):
        """
        Register windows when they are created.
        """
        # create the instance has usual
        instance = super(WindowMetaclass, cls).__call__(*args, **kwargs)

        # register the window if properties present
        cls.manager.add(instance)

        # return the instance
        return instance


class SDLWindow(object, metaclass=WindowMetaclass):
    def __init__(
        self,
        title,
        w_pos=(s.SDL_WINDOWPOS_UNDEFINED, s.SDL_WINDOWPOS_UNDEFINED),
        size=m.Vector(800, 480),
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

        # keep a trace of the identity of the window
        self.id = s.SDL_GetWindowID(self._win)

        s.SDL_GL_SetAttribute(s.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        s.SDL_GL_SetAttribute(s.SDL_GL_CONTEXT_MINOR_VERSION, 3)

        # set the opengl context of the window
        self._context = s.SDL_GL_CreateContext(self._win)

        self._x = 0.
        self._y = 30.0

        self._widget = []

        self._screensize = size

        self._mouseHandler = None

    def events(self, ev):
        # Deal with events linked to the window:
        logger.debug(
            "Inside window %d for event.", id(self._win)
        )

        # loop over methods and call them if the associated event occurred
        for key in ev._methods.keys():
            if ev._methods[key][0] and hasattr(self, key):
                getattr(self, key)(ev._methods[key][1])

    def makeCurrent(self):
        s.SDL_GL_MakeCurrent(self._win, self._context)

    def paintEvent(self, event):
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

        self.swap()

    def swap(self):
        s.SDL_GL_SwapWindow(self._win)

    def updateWindow(self):
        s.SDL_UpdateWindowSurface(self._win)

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

    def close(self):
        # remove the window in the register of window to display in the
        # event loop
        SDLWindow.manager.delete(self)

        # destroy the window with SDL
        s.SDL_DestroyWindow(
            self._win
        )

    def mouseReleaseEvent(self, event):
        """
        The window gives the release event to the child that has grabbed the
        press event before. Then the child that must handle the event is set to
        None, since nobody must get a move event when the mouse is released.
        """
        # check a child get the press event
        if self._mouseHandler:
            # inform it that the mouse is released
            self._mouseHandler.mouseReleaseEvent(event)

            # nobody can get the event
            self._mouseHandler = None

    def mousePressEvent(self, event):
        """
        The window find the widget handling the mouse press event with the
        position of the mouse in the window. Then the mouse press event is send
        to this widget. If he doesn't accept it, the event is passed
        recursively to the parent until a widget accept it.
        """
        # get the widget accepting the event
        widget = self._acceptMouse(self, self._widget, event)

        # check it is the window itself
        if widget is self:
            return self._mousePressEvent(event)

        # up in the tree while nobody accept the event, or we reach the root
        # (the window)
        while (not event.accepted):
            # the child accepting the event
            self._mouseHandler = widget

            # send press event to it
            self._mouseHandler.mousePressEvent(event)

            # the widget is the parent
            widget = widget.parent

            # check parent exist (not the window)
            if not widget:
                break

    def mouseMoveEvent(self, event):
        """
        The mouse move event is dispatched by the window to the child which as
        grabbed the mouse press event before. If the mouse has been released,
        the mouse move event is not dispatched to children.
        """
        # check the mouse is pressed and a child as grabbed the event
        if self._mouseHandler:
            # the widget handle this
            self._mouseHandler.mouseMoveEvent(event)

    def keyReleaseEvent(self, event):
        # loop over children widgets
        for widget in self._widget:
            # call the widget to see if he process the event
            widget.keyReleaseEvent(event)
            if event.accepted:
                break

    def keyPressEvent(self, event):
        # loop over children widgets
        for widget in self._widget:
            # call the widget to see if he process the event
            widget.keyPressEvent(event)
            if event.accepted:
                break

    def wheelEvent(self, event):
        # loop over children widgets
        for widget in self._widget:
            # call the widget to see if he process the event
            widget.wheelEvent(event)
            if event.accepted:
                break

    def closeEvent(self, event):
        self.close()

    def resizeEvent(self, event):
        s.SDL_SetWindowSize(self._win, *event.size)

    def focusInEvent(self, event):
        pass

    def focusOutEvent(self, event):
        pass

    def showEvent(self, event):
        """
        Called when the window is shown.
        """
        pass

    def exposeEvent(self, event):
        pass

    def _acceptMouse(self, widget, children, event):
        """
        To recursively know which widget is accepting a mouse press event.
        """
        # loop over widgets
        for child in children:
            # if the press is inside the widget, loop over its child
            if child.inside(event.x, event.y):
                # give to children to know which one must accept the press
                return self._acceptMouse(child, child._children, event)
        return widget

    def _mousePressEvent(self, event):
        pass

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._win_name

    @name.setter
    def name(self, val):
        s.SDL_SetWindowTitle(self._win, val.encode())
        self._win_name = val


# vim: set tw=79 :
