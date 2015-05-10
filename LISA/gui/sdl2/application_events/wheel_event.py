#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from .application_event import ApplicationEvent
from .types import Wheel

__all__ = ["WheelEvent"]

logger = logging.getLogger(__name__)

HANDLERS = {
    Wheel: "wheelEvent",
}


class WheelEvent(ApplicationEvent):
    """
    Class to handle and store informations on the wheel events.
    """
    def __init__(self, type):
        super(WheelEvent, self).__init__(type)

        self.dx = 0
        self.dy = 0

    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, dx):
        self._dx = dx

    @property
    def dy(self):
        return self._dy

    @dy.setter
    def dy(self, dy):
        self._dy = dy

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        if not type:
            return
        if type in HANDLERS:
            self._type = type
            return
        logger.error("The type {0} is not handled by WheelEvent".format(type))

    @property
    def handler(self):
        return HANDLERS[self.type]


# vim: set tw=79 :
