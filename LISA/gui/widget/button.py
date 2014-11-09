#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .fonts import Text
from ..utils.signals import Signal


class Button(Text):
    """
    A class to manage a button with action done when clicking on it.
    """

    def __init__(self, *args, **kwargs):

        # call parent
        super(Button, self).__init__(*args, **kwargs)

        # signal when clicking
        self.click = Signal()

    def mouseEvent(self, event):

        # compute the offset of the mouse cursor relative to the corner
        # of the widget, if not already pressed
        if self.inside(event.x, event.y):
            # left button of the mouse pressed
            if event[1]:
                # say it is pressed
                if not self._mousePress:
                    self._mousePress = True

            # the left button is released
            if not event[1] and self._mousePress:
                self._mousePress = False
                self.click()

            return True

# vim: set tw=79 :
