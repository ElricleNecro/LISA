#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import WindowEventProcessor
from ..application_events import ExposeEvent
from ..application_events import Expose

__all__ = ["WindowExposeEvent"]


class WindowExposeEvent(WindowEventProcessor):
    """
    To manage exposed event.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_EXPOSED

    @staticmethod
    def processEvent(event):
        return ExposeEvent(Expose)


# vim: set tw=79 :
