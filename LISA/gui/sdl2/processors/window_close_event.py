#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import WindowEventProcessor
from ..application_events import CloseEvent
from ..application_events import Close

__all__ = ["WindowCloseEvent"]


class WindowCloseEvent(WindowEventProcessor):
    """
    To manage close event.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_CLOSE

    @staticmethod
    def processEvent(event):
        return CloseEvent(Close)


# vim: set tw=79 :
