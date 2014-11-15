#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .fonts import Text
from .layout import HorizontalLayout
from ..utils.signals import Signal


class Button(HorizontalLayout):
    """
    A class to manage a button with action done when clicking on it.
    """

    def __init__(self, *args, **kwargs):

        # call parent
        super(Button, self).__init__(*args, **kwargs)

        # signal when clicking
        self.click = Signal()

        # set the text
        self._text = Text()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text.text = text
        self._text.size_hint = None
        if self._text not in self._children:
            self.addWidget(self._text)

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
