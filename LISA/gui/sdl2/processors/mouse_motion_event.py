#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2

from .processor_types import EventProcessor
from ..application_events import MouseEvent
from ..application_events import MouseMotion

__all__ = ["MouseMotionEvent"]


class MouseMotionEvent(EventProcessor):
    """
    To manage mouse motion event.
    """
    class Meta:
        register_type = sdl2.SDL_MOUSEMOTION

    @staticmethod
    def processEvent(event):
        ev = MouseEvent(MouseMotion, None)
        ev.dx = event.motion.xrel
        ev.dy = event.motion.yrel
        ev.x = event.motion.x
        ev.y = event.motion.y
        ev.windowId = event.motion.windowID
        return ev


# vim: set tw=79 :
