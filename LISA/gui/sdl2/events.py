#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2 as s
import ctypes
import logging

__all__ = ["_SDLInput_logger", "SDLInput"]

_SDLInput_logger = logging.getLogger('SDLInput')

ch = logging.StreamHandler()
ch.setFormatter(
    logging.Formatter(
        '%(name)s::%(asctime)s::%(levelname)s: %(message)s',
        "%d-%m-%Y %H:%M:%S"
    )
)

_SDLInput_logger.addHandler(ch)
# _SDLInput_logger.setLevel(logging.DEBUG)
_SDLInput_logger.setLevel(logging.WARNING)


class Keyboard(list):
    def __init__(self):
        super(Keyboard, self).__init__([False for i in range(s.SDL_NUM_SCANCODES)])


class Mouse(list):
    def __init__(self):
        super(Mouse, self).__init__([False for i in range(8)])

        self._x = 0.
        self._y = 0.

        self._xRel = 0.
        self._yRel = 0.

        class Wheel(object):
            dx = 0.
            dy = 0.

        self._wheel = Wheel()

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

    @property
    def wheel(self):
        return self._wheel


class Window(object):
    pass


class SDLInput(object):
    def __init__(self):
        self._mouse = Mouse()
        self._keys = Keyboard()

        self._end = False

        self._event = s.SDL_Event()
        self._methods = {
            "mouseEvent": False,
            "keyEvent": False,
        }

    def update(self):

        # say that we don't use any methods in the window
        for key in self._methods.keys():
            self._methods[key] = False
        self._resized = False

        # initiialize relative movement to null
        self._mouse.dx, self._mouse.dy = 0., 0.
        self._mouse.wheel.dx, self._mouse.wheel.dy = 0., 0.

        # window size
        self._window_size = (0., 0.)

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

                self._methods["keyEvent"] = True

            elif self._event.type == s.SDL_KEYUP:
                self._keys[self._event.key.keysym.scancode] = False

                self._methods["keyEvent"] = False

            elif self._event.type == s.SDL_MOUSEBUTTONDOWN:
                self._mouse[self._event.button.button] = True

                self._methods["mouseEvent"] = True

            elif self._event.type == s.SDL_MOUSEBUTTONUP:
                self._mouse[self._event.button.button] = False

                self._methods["mouseEvent"] = False

            elif self._event.type == s.SDL_MOUSEMOTION:
                self._mouse.dx = self._event.motion.xrel
                self._mouse.dy = self._event.motion.yrel

                self._methods["mouseEvent"] = True

            elif self._event.type == s.SDL_MOUSEWHEEL:
                self._mouse.wheel.dx = self._event.wheel.x
                self._mouse.wheel.dy = self._event.wheel.y

                self._methods["mouseEvent"] = True

            else:
                break

        self._mouse.x = self._event.motion.x
        self._mouse.y = self._event.motion.y


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

    def _showCursor(self, val):
        if type(val) == bool:
            if val:
                s.SDL_ShowCursor(s.SDL_ENABLE)
            else:
                s.SDL_ShowCursor(s.SDL_DISABLE)
        else:
            _SDLInput_logger.warn('ShowCursor must get a boolean!')

    showCursor = property(fset=_showCursor, doc="")


# vim: set tw=79 :
