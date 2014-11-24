#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .layout import VerticalLayout, HorizontalLayout
from .button import Button
from .fonts import Text


__all__ = ["Application"]


class Application(VerticalLayout):
    """
    A class for managing an application with title bar, action buttons and
    contents...
    """

    def __init__(self, *args, **kwargs):

        # get the layout for contents
        if "layout" in kwargs:
            layout = kwargs.pop("layout")
        else:
            layout = "vertical"

        super(Application, self).__init__(*args, **kwargs)

        # layout for the titlebar
        self.titlebar = HorizontalLayout()
        self.titlebar.size_hint_x = 1.
        self.titlebar.size_hint_y = None

        # layout for the content
        if layout.upper() == "VERTICAL":
            self.content = VerticalLayout()
        elif layout.upper() == "HORIZONTAL":
            self.content = HorizontalLayout()
        else:
            raise ValueError("No good content layout for application.")
        self.content.size_hint = 1.

        # the text for the title
        self.title = Text()
        self.title.size_hint = None
        self._title_container = VerticalLayout()
        self._title_container.size_hint_y = None
        self._title_container.size_hint_x = 1.
        self._title_container.padding = 0
        self._title_container.margin = 0
        self._title_container.addWidget(self.title)

        # add the text to the layout
        self.titlebar.addWidget(self._title_container)

        # create the button
        self.close = Button()
        self.close.size_hint = None
        self.close.text = "X"

        # add it to the layout
        self.titlebar.addWidget(self.close)

        # add title bar and content to the application
        super(Application, self).addWidget(self.titlebar)
        super(Application, self).addWidget(self.content)

        # add a padding for moving window
        self.padding = 5

    def addWidget(self, widget):
        """
        Add other widget to the vertical layout.
        """

        self.content.addWidget(widget)

    def mouseEvent(self, event):

        # call the parent
        if super(VerticalLayout, self).mouseEvent(event):
            return True

        # left button of the mouse pressed
        if event[1]:

            # compute the offset of the mouse cursor relative to the corner
            # of the widget, if not already pressed
            if not self._mousePress:
                self._mouse[0] = event.x
                self._mouse[1] = event.y
                self._mouseOffset = self._mouse - self._corner

            # check that we are inside or not the border used to resize the
            # widget
            if self._inside_border(event.x, event.y):
                if not self._mousePressBorders:
                    self._mouse[0] = event.x
                    self._mouse[1] = event.y
                    self._sizeOffset = self._size - self._mouse + self._corner
                self._mousePressBorders = True
            elif self.inside(event.x, event.y) and not self._mousePressBorders:
                self._mousePress = True

        # the left button is released
        if not event[1]:
            self._mousePress = False
            self._mousePressBorders = False

        if self._mousePressBorders:
            self.width = self._sizeOffset[0] + event.x - self._corner[0]
            self.height = self._sizeOffset[1] + event.y - self._corner[1]
            return True
        if self._mousePress:
            self.x = event.x - self._mouseOffset[0]
            self.y = event.y - self._mouseOffset[1]
            return True
# vim: set tw=79 :
