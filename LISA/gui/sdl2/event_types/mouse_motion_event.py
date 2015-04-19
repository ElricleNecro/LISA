#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["MouseMotionEvent"]


class MouseMotionEvent(EventType):
    """
    To manage mouse motion event.
    """
    __register_type__ = sdl2.SDL_MOUSEMOTION
    __event_method__ = "mouseEvent"

    def processEvent(self, event):
        super(MouseMotionEvent, self).processEvent(event)
        self.mouse.dx = event.motion.xrel
        self.mouse.dy = event.motion.yrel
        self.mouse.x = event.motion.x
        self.mouse.y = event.motion.y


# vim: set tw=79 :
