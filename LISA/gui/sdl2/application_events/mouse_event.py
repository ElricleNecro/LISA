#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from .application_event import ApplicationEvent
from .types import MouseUp
from .types import MouseDown
from .types import MouseMotion

__all__ = ["MouseEvent"]

logger = logging.getLogger(__name__)

HANDLERS = {
    MouseUp: "mouseReleaseEvent",
    MouseDown: "mousePressEvent",
    MouseMotion: "mouseMoveEvent",
}


class MouseEvent(ApplicationEvent):
    """
    Class to handle and store informations on the mouse events.
    """
    def __init__(self, type, button):
        super(MouseEvent, self).__init__(type)

        self.button = button
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0

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
        logger.error("The type {0} is not handled by MouseEvent".format(type))

    @property
    def button(self):
        return self._button

    @button.setter
    def button(self, button):
        self._button = button

    @property
    def handler(self):
        return HANDLERS[self.type]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

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


# vim: set tw=79 :
