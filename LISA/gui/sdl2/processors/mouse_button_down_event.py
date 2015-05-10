#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import EventProcessor
from ..application_events import MouseEvent
from ..application_events import MouseDown

__all__ = ["MouseDownEvent"]


class MouseDownEvent(EventProcessor):
    """
    To manage mouse down event.
    """
    class Meta:
        register_type = sdl2.SDL_MOUSEBUTTONDOWN

    @staticmethod
    def processEvent(event):
        ev = MouseEvent(MouseDown, event.button.button)
        ev.x = event.button.x
        ev.y = event.button.y
        ev.windowId = event.button.windowID
        return ev


# vim: set tw=79 :
