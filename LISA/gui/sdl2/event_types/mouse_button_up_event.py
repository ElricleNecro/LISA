#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["MouseButtonUpEvent"]


class MouseButtonUpEvent(EventType):
    """
    To manage mouse up event.
    """
    __register_type__ = sdl2.SDL_MOUSEBUTTONUP
    __event_method__ = "mouseEvent"

    def processEvent(self, event):
        super(MouseButtonUpEvent, self).processEvent(event)
        self.mouse[event.button.button] = False


# vim: set tw=79 :
