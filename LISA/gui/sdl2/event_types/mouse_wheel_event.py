#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["WheelEvent"]


class WheelEvent(EventType):
    """
    To manage wheel event.
    """
    __register_type__ = sdl2.SDL_MOUSEWHEEL
    __event_method__ = "wheelEvent"

    def processEvent(self, event):
        super(WheelEvent, self).processEvent(event)
        self.wheel.dx = event.wheel.x
        self.wheel.dy = event.wheel.y


# vim: set tw=79 :
