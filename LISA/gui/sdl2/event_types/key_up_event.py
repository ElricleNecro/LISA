#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["KeyUpEvent"]


class KeyUpEvent(EventType):
    """
    To manage key up event.
    """
    class Meta:
        register_type = sdl2.SDL_KEYUP
        event_method = "keyEvent"
        event_attribute = "keys"

    def processEvent(self, event):
        self.keys[event.key.keysym.scancode] = False
        super(KeyUpEvent, self).processEvent(event)


# vim: set tw=79 :
