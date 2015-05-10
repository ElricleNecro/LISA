#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from .application_event import ApplicationEvent
from .types import FocusIn
from .types import FocusOut

__all__ = ["FocusEvent"]

logger = logging.getLogger(__name__)

HANDLERS = {
    FocusIn: "focusInEvent",
    FocusOut: "focusOutEvent",
}


class FocusEvent(ApplicationEvent):
    """
    Class to handle and store informations on the focus events.
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
        logger.error("The type {0} is not handled by FocusEvent".format(type))

    @property
    def handler(self):
        return HANDLERS[self.type]


# vim: set tw=79 :
