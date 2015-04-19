#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["MouseButtonDownEvent"]


class MouseButtonDownEvent(EventType):
    """
    To manage mouse up event.
    """
    __register_type__ = sdl2.SDL_MOUSEBUTTONDOWN
    __event_method__ = "mouseEvent"

    def processEvent(self, event):
        super(MouseButtonDownEvent, self).processEvent(event)
        self.mouse[event.button.button] = True


# vim: set tw=79 :
