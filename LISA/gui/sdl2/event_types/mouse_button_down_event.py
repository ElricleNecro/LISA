#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .event_types import EventType

__all__ = ["MouseButtonDownEvent"]


class MouseButtonDownEvent(EventType):
    """
    To manage mouse up event.
    """
    class Meta:
        register_type = sdl2.SDL_MOUSEBUTTONDOWN
        event_method = "mouseEvent"
        event_attribute = "mouse"

    def processEvent(self, event):
        self.mouse[event.button.button] = True
        super(MouseButtonDownEvent, self).processEvent(event)


# vim: set tw=79 :
