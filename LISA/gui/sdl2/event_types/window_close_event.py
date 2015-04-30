#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2
from .event_types import WindowEventType

__all__ = ["WindowCloseEvent"]


class WindowCloseEvent(WindowEventType):
    """
    To manage window events.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_CLOSE
        event_method = "closeEvent"
        event_attribute = "window"

    def processEvent(self, event):
        self.window.id = event.window.windowID
        self.window.end = True
        super(WindowCloseEvent, self).processEvent(event)


# vim: set tw=79 :
