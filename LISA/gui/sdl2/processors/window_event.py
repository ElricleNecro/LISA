#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import EventProcessor
from .processor_types import WindowEventProcessor

__all__ = ["WindowEvent"]


class WindowEvent(EventProcessor):
    """
    To manage window events.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT

    def __init__(self, *args, **kwargs):
        super(WindowEvent, self).__init__(*args, **kwargs)

    @staticmethod
    def processEvent(event):
        kind = event.window.event
        if kind in WindowEventProcessor.manager:
            ev = WindowEventProcessor.manager[kind].processEvent(event)
            ev.windowId = event.window.windowID
            return ev


# vim: set tw=79 :
