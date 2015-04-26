#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2
from .event_types import WindowEventType

__all__ = ["WindowEnterEvent"]


class WindowEnterEvent(WindowEventType):
    """
    To manage window events.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_ENTER

    def processEvent(self, event):
        self.window.id = event.window.windowID


# vim: set tw=79 :
