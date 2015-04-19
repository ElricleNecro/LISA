#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["KeyDownEvent"]


class KeyDownEvent(EventType):
    """
    To manage key down event.
    """
    __register_type__ = sdl2.SDL_KEYDOWN
    __event_method__ = "keyEvent"

    def processEvent(self, event):
        super(KeyDownEvent, self).processEvent(event)
        self.keys[event.key.keysym.scancode] = True


# vim: set tw=79 :
