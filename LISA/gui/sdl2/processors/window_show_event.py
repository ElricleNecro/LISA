#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import WindowEventProcessor
from ..application_events import ShowEvent
from ..application_events import Show

__all__ = ["WindowShowEvent"]


class WindowShowEvent(WindowEventProcessor):
    """
    To manage resize event.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT_SHOWN

    @staticmethod
    def processEvent(event):
        return ShowEvent(Show)


# vim: set tw=79 :
