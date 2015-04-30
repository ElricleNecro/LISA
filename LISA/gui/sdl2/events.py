#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2 as s
import ctypes
import logging

from .event_types import EventType

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
        super(Keyboard, self).__init__(
            [False for i in range(s.SDL_NUM_SCANCODES)]
        )


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

    def reset(self):
        self.dx, self.dy = 0., 0.


class Window(object):
    def __init__(self):
        self.resized = False
        self.end = False
        self.windowSize = (0., 0.)
        self.id = None

    def reset(self):
        self.resized = False


class SDLInput(object):
    def __init__(self):
        self._event = s.SDL_Event()

        # create events
        self._createEvents()

    def _createEvents(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.wheel = Wheel()
        self.window = Window()

        for event in EventType.available_events.values():
            event(
                mouse=self.mouse,
                keys=self.keyboard,
                window=self.window,
                wheel=self.wheel,
            )

    def update(self):
        self.mouse.reset()
        self.window.reset()
        # loop over event in the queue
        while s.SDL_PollEvent(ctypes.byref(self._event)) != 0:
            if self._event.type in EventType.events:
                EventType.events[self._event.type].processEvent(self._event)
            else:
                break

    @property
    def keyboard(self):
        return self._keys

    @keyboard.setter
    def keyboard(self, keyboard):
        self._keys = keyboard

    @property
    def mouse(self):
        return self._mouse

    @mouse.setter
    def mouse(self, mouse):
        self._mouse = mouse

    @property
    def wheel(self):
        return self._wheel

    @wheel.setter
    def wheel(self, wheel):
        self._wheel = wheel

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window):
        self._window = window

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
