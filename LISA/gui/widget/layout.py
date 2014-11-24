#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .widget import Widget


__all__ = ["VerticalLayout", "HorizontalLayout"]


class BaseLayout(Widget):

    def __init__(self, *args, **kwargs):

        super(BaseLayout, self).__init__(*args, **kwargs)

        # indicate if already resizing the widget
        self._resizing = False

        # default padding null
        self.padding = 0
        self.margin = 0

    def addWidget(self, widget):
        """
        Add a widget to the list of children performing a pre processing to
        give the correct vertical layout to widgets.
        """

        # call parent to add correctly widget
        super(BaseLayout, self).addWidget(widget)

        # set minimal sizes
        self.minWidth = widget.minWidth
        self.minHeight = widget.minHeight

        # set width and height
        self.width = widget.width
        self.height = widget.height

    @property
    def minWidth(self):
        return self._minWidth

    @minWidth.setter
    def minWidth(self, minWidth):
        # if the size is superior to the already defined min
        if minWidth >= float(self._minWidth - self.padding_x.sum()):
            self._minWidth = float(minWidth + self.padding_x.sum())
        else:

            # get the maximal minimal width of children
            mintmp = 0
            for widget in self._children:
                if widget.minWidth > mintmp:
                    mintmp = float(widget.minWidth + widget.margin_x.sum())

            # check size compared to actual size
            if mintmp >= minWidth:
                self._minWidth = mintmp
            else:
                self._minWidth = minWidth

        # call parent
        if self.parent is not None:
            self.parent.minWidth = float(self.minWidth + self.margin_x.sum())

        # update width
        if self.width < self._minWidth:
            self.width = self._minWidth

    @property
    def minHeight(self):
        return self._minHeight

    @minHeight.setter
    def minHeight(self, minHeight):
        # if the size is superior to the already defined min
        if minHeight >= float(self._minHeight - self.padding_y.sum()):
            self._minHeight = float(minHeight + self.padding_y.sum())
        else:

            # get the maximal minimal height of children
            mintmp = 0
            for widget in self._children:
                if widget.minHeight > mintmp:
                    mintmp = float(widget.minHeight + widget.margin_y.sum())

            # check size compared to actual size
            if mintmp >= minHeight:
                self._minHeight = mintmp
            else:
                self._minHeight = minHeight

        # call parent
        if self.parent is not None:
            self.parent.minHeight = float(self.minHeight + self.margin_y.sum())

        # check height
        if self.height < self._minHeight:
            self.height = self._minHeight

    @property
    def x(self):
        return self._corner[0]

    @x.setter
    def x(self, x):

        # store old position
        old = self._corner[0]

        # set as parent
        super(BaseLayout, self.__class__).x.fset(self, x)

        # loop over children for new position
        for widget in self._children:
            widget.x += x - old

    @property
    def y(self):
        return self._corner[1]

    @y.setter
    def y(self, y):

        # store old position
        old = self._corner[1]

        # set as parent
        super(BaseLayout, self.__class__).y.fset(self, y)

        # loop over children for new position
        for widget in self._children:
            widget.y += y - old


class VerticalLayout(BaseLayout):

    def _widget_position(self, widget):
        return self.y + self.padding_top + self._total + widget.margin_top

    @property
    def width(self):
        return self._size[0]

    @width.setter
    def width(self, width):

        if self._resizing:
            return

        self._resizing = True

        super(VerticalLayout, self.__class__).width.fset(self, width)

        # loop over children to resize the width
        for widget in self._children:

            # set the offset of the position to zero
            offset = 0

            # change the size hint with margin if specified
            if widget.size_hint_x is not None:
                widget.width = int(widget.size_hint_x * float(
                    self._size[0] - self.padding_x.sum()
                ) - widget.margin_x.sum())

            else:
                offset = int(0.5 * float(
                    self._size[0] - widget.width
                ) - self.padding_left - self.margin_left)

            # set the position according to padding and margin
            widget.x = self.x + self.padding_left + widget.margin_left + offset

        # indicate not resizing
        self._resizing = False

    @property
    def height(self):
        return self._size[1]

    @height.setter
    def height(self, height):

        if self._resizing:
            return

        self._resizing = True

        super(VerticalLayout, self.__class__).height.fset(self, height)

        # init the total height of childrens
        self._total = 0
        total_static = 0

        # compute total static size
        for widget in self._children:
            if widget.size_hint_y is None:
                total_static += int(widget.height + widget.margin_y.sum())

        # loop over children to resize the width
        for widget in self._children:

            # set the position according to padding and margin
            widget.y = self._widget_position(widget)

            # change the size hint with margin if specified
            if widget.size_hint_y is not None:
                widget.height = int(widget.size_hint_y * float(
                    self._size[1] - self.padding_y.sum() - total_static
                ) - widget.margin_y.sum())

            # add to the total children height the new widget and its margin
            self._total += widget.height + widget.margin_y.sum()

        # not resizing
        self._resizing = False

    @property
    def minHeight(self):
        return self._minHeight

    @minHeight.setter
    def minHeight(self, minHeight):
        # get the minimal height of all children
        self._minHeight = float(self.padding_y.sum())
        for widget in self._children:
            self._minHeight += float(widget.minHeight + widget.margin_y.sum())

        # call parent
        if self.parent is not None:
            self.parent.minHeight = float(self.minHeight + self.margin_y.sum())

        # check height
        if self.height < self._minHeight:
            self.height = self._minHeight


class HorizontalLayout(BaseLayout):

    def _widget_position(self, widget):
        return self.x + self.padding_left + self._total + widget.margin_left

    @property
    def height(self):
        return self._size[1]

    @height.setter
    def height(self, height):

        if self._resizing:
            return

        self._resizing = True

        super(HorizontalLayout, self.__class__).height.fset(self, height)

        # loop over children to resize the height
        for widget in self._children:

            # set the offset of the position to zero
            offset = 0

            # change the size hint with margin if specified
            if widget.size_hint_y is not None:
                widget.height = int(widget.size_hint_y * float(
                    self._size[1] - self.padding_y.sum()
                ) - widget.margin_y.sum())

            else:
                offset = int(0.5 * float(
                    self._size[1] - widget.height
                ) - self.padding_top - self.margin_top)

            # set the position according to padding and margin
            widget.y = self.y + self.padding_top + widget.margin_top + offset

        # indicate not resizing
        self._resizing = False

    @property
    def width(self):
        return self._size[0]

    @width.setter
    def width(self, width):

        if self._resizing:
            return

        self._resizing = True

        super(HorizontalLayout, self.__class__).width.fset(self, width)

        # init the total width of childrens
        self._total = 0
        total_static = 0

        # compute total static size
        for widget in self._children:
            if widget.size_hint_x is None:
                total_static += int(widget.width + widget.margin_x.sum())

        # loop over children to resize the width
        for widget in self._children:

            # set the position according to padding and margin
            widget.x = self._widget_position(widget)

            # change the size hint with margin if specified
            if widget.size_hint_x is not None:
                widget.width = int(widget.size_hint_x * float(
                    self._size[0] - self.padding_x.sum() - total_static
                ) - widget.margin_x.sum())

            # add to the total children width the new widget and its margin
            self._total += widget.width + widget.margin_x.sum()

        # not resizing
        self._resizing = False

    @property
    def minWidth(self):
        return self._minWidth

    @minWidth.setter
    def minWidth(self, minWidth):
        # get the minimal height of all children
        self._minWidth = float(self.padding_x.sum())
        for widget in self._children:
            self._minWidth += float(widget.minWidth + widget.margin_x.sum())

        # call parent
        if self.parent is not None:
            self.parent.minWidth = float(self.minWidth + self.margin_x.sum())

        # check height
        if self.width < self._minWidth:
            self.width = self.width
# vim: set tw=79 :
