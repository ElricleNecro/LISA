#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sdl2
from .event_types import EventType
from .event_types import WindowEventType

__all__ = ["WindowEvent"]


class WindowEvent(EventType):
    """
    To manage window events.
    """
    class Meta:
        register_type = sdl2.SDL_WINDOWEVENT
        event_method = "resizeEvent"
        event_attribute = "window"

    def __init__(self, *args, **kwargs):
        super(WindowEvent, self).__init__(*args, **kwargs)

        # create window events
        self._createWindowEvents()

    def _createWindowEvents(self):
        """
        Create window events type.
        """
        for event in WindowEventType.available_events.values():
            event(
                mouse=self.mouse,
                keys=self.keys,
                window=self.window,
                wheel=self.wheel,
            )

    def processEvent(self, event):
        if event.window.event in WindowEventType.events:
            WindowEventType.events[event.window.event].processEvent(event)


# vim: set tw=79 :
