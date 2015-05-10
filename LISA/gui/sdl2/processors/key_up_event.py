#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import EventProcessor
from ..application_events import KeyEvent
from ..application_events import KeyUp

__all__ = ["KeyUpEvent"]


class KeyUpEvent(EventProcessor):
    """
    To manage key up event from the SDL.
    """
    class Meta:
        register_type = sdl2.SDL_KEYUP

    @staticmethod
    def processEvent(event):
        ev = KeyEvent(KeyUp, event.key.keysym.scancode)
        ev.windowId = event.key.windowID
        return ev


# vim: set tw=79 :
