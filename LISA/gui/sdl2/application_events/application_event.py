#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ["ApplicationEvent"]


class ApplicationEvent(object):
    """
    Base class for the event used by the application.
    """
    def __init__(self, type):
        """
        Some flags used by the event.
        """
        self.ignore()
        self.type = type
        self._handler = None
        self.windowId = None

    def accept(self):
        """
        Indicate that the event should not be propagated to parents.
        """
        self._accepted = True

    def ignore(self):
        """
        Indicate that the event should be propagated to the parent.
        """
        self._accepted = False

    @property
    def accepted(self):
        return self._accepted

    @accepted.setter
    def accepted(self, accepted):
        self._accepted = accepted

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, handler):
        self._handler = handler

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def windowId(self):
        return self._windowId

    @windowId.setter
    def windowId(self, windowId):
        self._windowId = windowId


# vim: set tw=79 :
