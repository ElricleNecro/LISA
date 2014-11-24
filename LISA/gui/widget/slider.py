#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .layout import VerticalLayout, HorizontalLayout
from .widget import Widget
from LISA.gui.utils.signals import Signal


__all__ = ["VerticalSlider", "HorizontalSlider"]


class VerticalSlider(VerticalLayout):

    def __init__(self, *args, **kwargs):

        # init the parent
        super(VerticalSlider, self).__init__(*args, **kwargs)

        # create a widget for the moving block
        self.block = Widget()

        # set a minimal width for to be fixed
        self.block.minWidth = 20
        self.block.width = 20
        self.block.minHeight = 30
        self.block.height = 30
        self.block.padding = 0
        self.block.margin = 0

        # set another background color for the block
        self.block.bgcolor = 1., 0., 0., 0.7

        # force the size hint
        self.size_hint_x = None
        self.size_hint_y = 1.

        # the value of the slide
        self._slideValue = 0.

        # add the block to the container
        self.addWidget(self.block)

        # signal when the value is updated
        self.changedSlider = Signal()

    def mouseEvent(self, event):

        # left button of the mouse pressed
        if event[1]:

            # compute the offset of the mouse cursor relative to the corner
            # of the widget, if not already pressed
            if not self._mousePress:
                self._mouse[0] = event.x
                self._mouse[1] = event.y
                self._mouseOffset = self._mouse - self.block._corner

            # check that we are inside the block
            if self.block.inside(event.x, event.y):
                # indicate that it is pressed
                self._mousePress = True

        # the left button is released
        if not event[1]:
            self._mousePress = False

        if self._mousePress:
            # compute the position of the left edge of the block
            position = event.y - self._mouseOffset[1]

            # check inside the parent container in top
            parent_edge = self.y + self.padding_top
            if position < parent_edge:
                position = parent_edge

            # check inside the parent container in top
            parent_edge = (
                self.y + self.height - self.padding_bottom - self.block.height
            )
            if (position > parent_edge):
                position = parent_edge

            # compute the value of the position of the slide between 0 and 1
            self.slideValue = (position - self.y - self.padding_top) / float(
                self.height - self.padding_y.sum() - self.block.height
            )

            # set the position of the block inside
            self.block.y = self._widget_position(None)

            # indicate that the event is intercepted
            return True

    def _widget_position(self, widget):
        return self.y + self.padding_top + self.slideValue * float(
            self.height - self.padding_y.sum() - self.block.height
        )

    @property
    def slideValue(self):
        return self._slideValue

    @slideValue.setter
    def slideValue(self, slideValue):
        self._slideValue = slideValue
        self.changedSlider(self._slideValue)


class HorizontalSlider(HorizontalLayout):

    def __init__(self, *args, **kwargs):

        # init the parent
        super(HorizontalSlider, self).__init__(*args, **kwargs)

        # create a widget for the moving block
        self.block = Widget()

        # set a minimal width for to be fixed
        self.block.minWidth = 20
        self.block.width = 20
        self.block.minHeight = 30
        self.block.height = 30
        self.block.padding = 0
        self.block.margin = 0

        # set another background color for the block
        self.block.bgcolor = 1., 0., 0., 0.7

        # force the size hint
        self.size_hint_y = None
        self.size_hint_x = 1.

        # the value of the slide
        self._slideValue = 0.

        # add the block to the container
        self.addWidget(self.block)

        # signal when the value is updated
        self.changedSlider = Signal()

    def mouseEvent(self, event):

        # left button of the mouse pressed
        if event[1]:

            # compute the offset of the mouse cursor relative to the corner
            # of the widget, if not already pressed
            if not self._mousePress:
                self._mouse[0] = event.x
                self._mouse[1] = event.y
                self._mouseOffset = self._mouse - self.block._corner

            # check that we are inside the block
            if self.block.inside(event.x, event.y):
                # indicate that it is pressed
                self._mousePress = True

        # the left button is released
        if not event[1]:
            self._mousePress = False

        if self._mousePress:
            # compute the position of the left edge of the block
            position = event.x - self._mouseOffset[0]

            # check inside the parent container in left
            parent_edge = self.x + self.padding_left
            if position < parent_edge:
                position = parent_edge

            # check inside the parent container in right
            parent_edge = (
                self.x + self.width - self.padding_right - self.block.width
            )
            if (position > parent_edge):
                position = parent_edge

            # compute the value of the position of the slide between 0 and 1
            self.slideValue = (position - self.x - self.padding_left) / float(
                self.width - self.padding_x.sum() - self.block.width
            )

            # set the position of the block inside
            self.block.x = self._widget_position(None)

            # indicate that the event was intercepted
            return True

    def _widget_position(self, widget):
        return self.x + self.padding_left + self.slideValue * float(
            self.width - self.padding_x.sum() - self.block.width
        )

    @property
    def slideValue(self):
        return self._slideValue

    @slideValue.setter
    def slideValue(self, slideValue):
        self._slideValue = slideValue
        self.changedSlider(self._slideValue)
# vim: set tw=79 :
