#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["KeyUpEvent"]


class KeyUpEvent(EventType):
    """
    To manage key up event.
    """
    __register_type__ = sdl2.SDL_KEYUP
    __event_method__ = "keyEvent"

    def processEvent(self, event):
        super(KeyUpEvent, self).processEvent(event)
        self.keys[event.key.keysym.scancode] = False


# vim: set tw=79 :
