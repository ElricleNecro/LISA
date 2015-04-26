#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2
from .event_types import WindowEventType

__all__ = ["WindowResizeEvent"]


class WindowResizeEvent(WindowEventType):
    """
    To manage window events.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_RESIZED
        event_method = "resizeEvent"
        event_attribute = "window"

    def processEvent(self, event):
        self.window.id = event.window.windowID
        self.window.resized = True
        self.window.windowSize = (
            event.window.data1,
            event.window.data2,
        )
        super(WindowResizeEvent, self).processEvent(event)


# vim: set tw=79 :
