#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2 as s
import ctypes
import logging

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


class SDLInput(object):
    def __init__(self):
        self._mouse = [False for i in range(8)]
        self._keys = [False for i in range(s.SDL_NUM_SCANCODES)]

        self._end = False

        self._x = 0.
        self._y = 0.

        self._xRel = 0.
        self._yRel = 0.

        self._event = s.SDL_Event()

    def update(self):
        self._xRel, self._yRel = 0., 0.
        while s.SDL_PollEvent(ctypes.byref(self._event)) != 0:

            self._id = self._event.window.windowID

            if self._event.type == s.SDL_WINDOWEVENT:
                if self._event.window.event == s.SDL_WINDOWEVENT_CLOSE:
                    self._end = True
                break
            elif self._event.type == s.SDL_KEYDOWN:
                self._keys[self._event.key.keysym.scancode] = True
                break
            elif self._event.type == s.SDL_KEYUP:
                self._keys[self._event.key.keysym.scancode] = False
                break
            elif self._event.type == s.SDL_MOUSEBUTTONDOWN:
                self._mouse[self._event.button.button] = True
                break
            elif self._event.type == s.SDL_MOUSEBUTTONUP:
                self._mouse[self._event.button.button] = False
                break
            elif self._event.type == s.SDL_MOUSEMOTION:
                self._x = self._event.motion.x
                self._y = self._event.motion.y

                self._xRel = self._event.motion.xrel
                self._yRel = self._event.motion.yrel
                break
            else:
                break

    @property
    def id(self):
        return self._id

    @property
    def End(self):
        return self._end

    @property
    def getKey(self):
        return self._keys

    @property
    def getButton(self):
        return self._mouse

    @property
    def getMousePos(self):
        return (self._x, self._y)

    @property
    def getMouseMove(self):
        return (self._xRel, self._yRel)

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
