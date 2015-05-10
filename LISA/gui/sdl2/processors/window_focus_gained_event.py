#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import WindowEventProcessor
from ..application_events import FocusEvent
from ..application_events import FocusIn

__all__ = ["WindowFocusInEvent"]


class WindowFocusInEvent(WindowEventProcessor):
    """
    To manage focus in event.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_FOCUS_GAINED

    @staticmethod
    def processEvent(event):
        return FocusEvent(FocusIn)


# vim: set tw=79 :
