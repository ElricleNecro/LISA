#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2
from .event_types import EventType

__all__ = ["WindowEvent"]


class WindowEvent(EventType):
    """
    To manage window events.
    """
    __register_type__ = sdl2.SDL_WINDOWEVENT
    __event_method__ = "resizeEvent"

    def processEvent(self, event):
        super(WindowEvent, self).processEvent(event)
        self.window.id = event.window.windowID
        if event.window.event == sdl2.SDL_WINDOWEVENT_CLOSE:
            self.window.end = True

        elif event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
            self.window.resized = True
            self.window.windowSize = (
                event.window.data1,
                event.window.data2,
            )


# vim: set tw=79 :
