#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import EventProcessor
from ..application_events import KeyEvent
from ..application_events import KeyDown

__all__ = ["KeyDownEvent"]


class KeyDownEvent(EventProcessor):
    """
    To manage key down event from the SDL.
    """
    class Meta:
        register_type = sdl2.SDL_KEYDOWN

    @staticmethod
    def processEvent(event):
        ev = KeyEvent(KeyDown, event.key.keysym.scancode)
        ev.windowId = event.key.windowID
        return ev


# vim: set tw=79 :
