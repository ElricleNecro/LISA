#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["KeyDownEvent"]


class KeyDownEvent(EventType):
    """
    To manage key down event.
    """
    class Meta:
        register_type = sdl2.SDL_KEYDOWN
        event_method = "keyEvent"
        event_attribute = "keys"

    def processEvent(self, event):
        self.keys[event.key.keysym.scancode] = True
        super(KeyDownEvent, self).processEvent(event)


# vim: set tw=79 :
