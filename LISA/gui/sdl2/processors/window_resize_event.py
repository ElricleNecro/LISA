#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import WindowEventProcessor
from ..application_events import ResizeEvent
from ..application_events import Resize

__all__ = ["WindowResizeEvent"]


class WindowResizeEvent(WindowEventProcessor):
    """
    To manage resize event.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_RESIZED

    @staticmethod
    def processEvent(event):
        return ResizeEvent(Resize, (event.window.data1, event.window.data2))


# vim: set tw=79 :
