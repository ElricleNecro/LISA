#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import EventProcessor
from ..application_events import MouseEvent
from ..application_events import MouseUp

__all__ = ["MouseUpEvent"]


class MouseUpEvent(EventProcessor):
    """
    To manage mouse up event.
    """
    class Meta:
        register_type = sdl2.SDL_MOUSEBUTTONUP

    @staticmethod
    def processEvent(event):
        ev = MouseEvent(MouseUp, event.button.button)
        ev.x = event.button.x
        ev.y = event.button.y
        ev.windowId = event.button.windowID
        return ev


# vim: set tw=79 :
