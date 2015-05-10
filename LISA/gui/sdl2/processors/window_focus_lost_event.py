#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import WindowEventProcessor
from ..application_events import FocusEvent
from ..application_events import FocusOut

__all__ = ["WindowFocusOutEvent"]


class WindowFocusOutEvent(WindowEventProcessor):
    """
    To manage focus in event.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_FOCUS_LOST

    @staticmethod
    def processEvent(event):
        return FocusEvent(FocusOut)


# vim: set tw=79 :
