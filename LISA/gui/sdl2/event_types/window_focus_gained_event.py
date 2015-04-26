#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2
from .event_types import WindowEventType

__all__ = ["WindowFocusGainedEvent"]


class WindowFocusGainedEvent(WindowEventType):
    """
    To manage window events.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_FOCUS_GAINED

    def processEvent(self, event):
        self.window.id = event.window.windowID


# vim: set tw=79 :
