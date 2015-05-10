#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import EventProcessor
from ..application_events import WheelEvent
from ..application_events import Wheel

__all__ = ["WheelEvent"]


class WheelProcessorEvent(EventProcessor):
    """
    To manage wheel event.
    """
    class Meta:
        register_type = sdl2.SDL_MOUSEWHEEL

    @staticmethod
    def processEvent(event):
        ev = WheelEvent(Wheel)
        ev.dx = event.wheel.x
        ev.dy = event.wheel.y
        ev.windowId = event.wheel.windowID
        return ev


# vim: set tw=79 :
