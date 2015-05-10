#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from .application_event import ApplicationEvent
from .types import Resize

__all__ = ["ResizeEvent"]

logger = logging.getLogger(__name__)

HANDLERS = {
    Resize: "resizeEvent",
}


class ResizeEvent(ApplicationEvent):
    """
    Class to handle and store informations on the wheel events.
    """
    def __init__(self, type, size):
        super(ResizeEvent, self).__init__(type)
        self.size = size

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

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
        logger.error("The type {0} is not handled by ResizeEvent".format(type))

    @property
    def handler(self):
        return HANDLERS[self.type]


# vim: set tw=79 :
