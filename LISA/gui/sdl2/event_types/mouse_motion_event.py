#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["MouseMotionEvent"]


class MouseMotionEvent(EventType):
    """
    To manage mouse motion event.
    """
    class Meta:
        register_type = sdl2.SDL_MOUSEMOTION
        event_method = "mouseEvent"
        event_attribute = "mouse"

    def processEvent(self, event):
        self.mouse.dx = event.motion.xrel
        self.mouse.dy = event.motion.yrel
        self.mouse.x = event.motion.x
        self.mouse.y = event.motion.y
        super(MouseMotionEvent, self).processEvent(event)


# vim: set tw=79 :
