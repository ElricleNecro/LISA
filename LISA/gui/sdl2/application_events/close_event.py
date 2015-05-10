#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from .application_event import ApplicationEvent
from .types import Close

__all__ = ["CloseEvent"]

logger = logging.getLogger(__name__)

HANDLERS = {
    Close: "closeEvent",
}


class CloseEvent(ApplicationEvent):
    """
    Class to handle and store informations on the wheel events.
    """
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
        logger.error("The type {0} is not handled by CloseEvent".format(type))

    @property
    def handler(self):
        return HANDLERS[self.type]


# vim: set tw=79 :
