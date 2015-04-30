#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["WheelEvent"]


class WheelEvent(EventType):
    """
    To manage wheel event.
    """
    class Meta:
        register_type = sdl2.SDL_MOUSEWHEEL
        event_method = "wheelEvent"
        event_attribute = "wheel"

    def processEvent(self, event):
        self.wheel.dx = event.wheel.x
        self.wheel.dy = event.wheel.y
        super(WheelEvent, self).processEvent(event)


# vim: set tw=79 :
