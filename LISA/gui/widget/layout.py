#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .widget import Widget


__all__ = ["VerticalLayout", "HorizontalLayout"]


class VerticalLayout(Widget):

    def __init__(self, *args, **kwargs):

        super(VerticalLayout, self).__init__(*args, **kwargs)

        # call the method when powition is updated
        self.changedPosition.connect(self._update)
        self.changedPadding.connect(self._update)
        self.changedWidth.connect(self._update)
        self.changedHeight.connect(self._update)

        # indicate if already resizing the widget
        self._resizing = False

        # default padding null
        self.padding = 0.
        self.margin = 0.

    def addWidget(self, widget):
        """
        Add a widget to the list of children performing a pre processing to
        give the correct vertical layout to widgets.
        """

        # connect the widget to the position updater
        widget.changedMargin.connect(self._update)
        widget.changedWidth.connect(self._update)
        widget.changedHeight.connect(self._update)

        # call parent to add correctly widget
        super(VerticalLayout, self).addWidget(widget)

        # update
        self._update()

    def _update(self, *args, **kwargs):

        # check if already computing a resize
        if self._resizing:
            return

        # indicate that it is resizing
        self._resizing = True

        # init the total height of childrens
        self._total = 0
        self._total_min = 0
        total_static = 0

        # compute total static size
        for widget in self._children:
            if widget.size_hint_y is None:
                total_static += int(widget.height + widget.margin_y.sum())

        # loop over children
        for widget in self._children:

            # set the offset of the position to zero
            offset = 0

            # change the size hint with margin if specified
            if widget.size_hint_x is not None:
                widget.width = int(widget.size_hint_x * float(
                    self.width - self.padding_x.sum()
                ) - widget.margin_x.sum())

            else:
                offset = int(0.5 * float(
                    self.width - widget.width
                ) - self.padding_left - self.margin_left)

            # set the position according to padding and margin
            widget.x = self.x + self.padding_left + widget.margin_left + offset

            # set the position according to padding and margin
            widget.y = (
                self.y + self.padding_top + self._total + widget.margin_top
            )

            # change the size hint with margin if specified
            if widget.size_hint_y is not None:
                widget.height = int(widget.size_hint_y * float(
                    self.height - self.padding_y.sum() - total_static
                ) - widget.margin_y.sum())

            # add to the total children height the new widget and its margin
            self._total_min += widget.minHeight + widget.margin_y.sum()
            self._total += widget.height + widget.margin_y.sum()

            self.minWidth = max(
                widget.minWidth + widget.margin_x.sum() + self.padding_x.sum(),
                self.minWidth,
            )
            self.width = max(widget.width, self.width)

        self.minHeight = self._total_min + self.padding_y.sum()
        self.height = self._total + self.padding_y.sum()

        # end of resizing
        self._resizing = False


class HorizontalLayout(Widget):

    def __init__(self, *args, **kwargs):

        super(HorizontalLayout, self).__init__(*args, **kwargs)

        # call the method when powition is updated
        self.changedPosition.connect(self._update)
        self.changedPadding.connect(self._update)
        self.changedWidth.connect(self._update)
        self.changedHeight.connect(self._update)

        # indicate if already resizing the widget
        self._resizing = False

        # default padding
        self.padding = 0
        self.margin = 0.

    def addWidget(self, widget):
        """
        Add a widget to the list of children performing a pre processing to
        give the correct vertical layout to widgets.
        """

        # connect the widget to the position updater
        widget.changedMargin.connect(self._update)
        widget.changedWidth.connect(self._update)
        widget.changedHeight.connect(self._update)

        # call parent to add correctly widget
        super(HorizontalLayout, self).addWidget(widget)

        # update
        self._update()

    def _update(self, *args, **kwargs):

        # check if already resizing
        if self._resizing:
            return

        # indicate that we are resizing
        self._resizing = True

        # init the total height of childrens
        self._total = 0.
        self._total_min = 0.
        total_static = 0.

        # compute total static size
        for widget in self._children:
            if widget.size_hint_x is None:
                total_static += int(widget.width + widget.margin_x.sum())

        # loop over children
        for widget in self._children:

            # init the offset in positioning
            offset = 0.

            # change the size hint with margin if specified
            if widget.size_hint_y is not None:
                widget.height = widget.size_hint_y * float(
                    self.height - self.padding_y.sum()
                ) - widget.margin_y.sum()

            else:
                offset = 0.5 * float(
                    self.height - widget.height
                ) - self.padding_top - self.margin_top

            # set the position according to padding and margin
            widget.y = self.y + self.padding_top + widget.margin_top + offset

            # set the position according to padding and margin
            widget.x = (
                self.x + self.padding_left + self._total + widget.margin_left
            )

            # change the size hint with margin if specified
            if widget.size_hint_x is not None:
                widget.width = widget.size_hint_x * float(
                    self.width - self.padding_x.sum() - total_static
                ) - widget.margin_x.sum()

            # add to the total children height the new widget and its margin
            self._total_min += widget.minWidth + widget.margin_x.sum()
            self._total += widget.width + widget.margin_x.sum()

            self.minHeight = max(
                widget.minHeight + widget.margin_y.sum() +
                self.padding_y.sum(),
                self.minHeight,
            )
            self.height = max(widget.height, self.height)

        self.minWidth = self._total_min + self.padding_x.sum()
        self.width = self._total + self.padding_x.sum()

        # end of resizing
        self._resizing = False

# vim: set tw=79 :
