#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from .application_event import ApplicationEvent
from .types import Paint

__all__ = ["PaintEvent"]

logger = logging.getLogger(__name__)

HANDLERS = {
    Paint: "paintEvent",
}


class PaintEvent(ApplicationEvent):
    """
    Class to handle and store informations on the wheel events.
    """
    def __init__(self, type, world):
        super(PaintEvent, self).__init__(type)
        self.world = world

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
        logger.error("The type {0} is not handled by PaintEvent".format(type))

    @property
    def handler(self):
        return HANDLERS[self.type]

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, world):
        self._world = world


# vim: set tw=79 :
