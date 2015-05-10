#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from .application_event import ApplicationEvent
from .types import KeyUp
from .types import KeyDown

__all__ = ["KeyEvent"]

logger = logging.getLogger(__name__)

HANDLERS = {
    KeyUp: "keyReleaseEvent",
    KeyDown: "keyPressEvent",
}


class KeyEvent(ApplicationEvent):
    """
    Class to handle and store informations on the key events.
    """
    def __init__(self, type, key):
        super(KeyEvent, self).__init__(type)

        self.key = key

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
        logger.error("The type {0} is not handled by KeyEvent".format(type))

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def handler(self):
        return HANDLERS[self.type]


# vim: set tw=79 :
