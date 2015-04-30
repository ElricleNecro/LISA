#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2
from .event_types import WindowEventType

__all__ = ["WindowFocusLostEvent"]


class WindowFocusLostEvent(WindowEventType):
    """
    To manage window events.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_FOCUS_LOST

    def processEvent(self, event):
        self.window.id = None


# vim: set tw=79 :
