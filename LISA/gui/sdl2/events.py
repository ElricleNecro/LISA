#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2 as s
import ctypes
import logging

from .event_types import EventType

__all__ = ["SDLInput"]

logger = logging.getLogger(__name__)


class Keyboard(list):
    """
    Structure used by windows to get informations on the corresponding keyboard
    event.
    """
    def __init__(self):
        """
        Init some properties of the structure. Store the list of available
        keys.
        """
        super(Keyboard, self).__init__(
            [False for i in range(s.SDL_NUM_SCANCODES)]
        )


class Wheel(object):
    """
    Structure used by windows to get informations on the corresponding wheel
    event.
    """
    dx = 0.
    dy = 0.


class Mouse(list):
    """
    Structure used by windows to get informations on the corresponding mouse
    event.
    """
    def __init__(self):
        """
        Init some properties of the structure.
        """
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
        """
        Reset the state of the structure.
        """
        self.dx, self.dy = 0., 0.


class Window(object):
    """
    Structure used by windows to get informations on the corresponding window
    event.
    """
    def __init__(self):
        """
        Init some properties of the structure.
        """
        self.resized = False
        self.end = False
        self.windowSize = (0., 0.)
        self.id = None

    def reset(self):
        """
        Reset the state of the structure.
        """
        self.resized = False


class SDLInput(object):
    def __init__(self):
        """
        Get the object for managing SDL events and create SDL events processors
        and event structures used by windows.
        """
        # SDL event managers
        self._event = s.SDL_Event()

        # create events
        self._createEvents()

    def _createEvents(self):
        """
        Responsible to create the structures containing informations on events
        that the window should handle.

        Then, loop over defined derived EventType classes by the user, passing
        it the event structures as attribute to the instances of EventType.
        """
        # create structures for informations of events, used by windows
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.wheel = Wheel()
        self.window = Window()

        # instantiate the derived EventType, with the event structures
        for event in EventType.available_events.values():
            event(
                mouse=self.mouse,
                keys=self.keyboard,
                window=self.window,
                wheel=self.wheel,
            )

    def update(self):
        """
        Responsible to process SDL events in the queue.
        """
        # reset event structures
        self.mouse.reset()
        self.window.reset()

        # loop over event in the queue
        while s.SDL_PollEvent(ctypes.byref(self._event)) != 0:
            # call the good event processor instance, by getting it from the
            # mapping in the manager
            if self._event.type in EventType.events:
                # process the SDL event with the good type
                EventType.events[self._event.type].processEvent(self._event)

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


# vim: set tw=79 :
