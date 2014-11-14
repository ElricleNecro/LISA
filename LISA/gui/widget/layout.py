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

    def addWidget(self, widget):
        """
        Add a widget to the list of children performing a pre processing to
        give the correct vertical layout to widgets.
        """

        # call parent to add correctly widget
        super(VerticalLayout, self).addWidget(widget)

        # update positions
        self._update()

        # connect the widget to the position updater
        widget.changedMargin(self._update)

    def _update(self, *args, **kwargs):
        """
        Connected to the signal emitted when the position of the container
        changed.
        """

        # init the total height of childrens
        total = 0.
        total_min = 0.
        total_static = 0.

        # compute total static size
        for widget in self._children:
            if widget.size_hint_y is None:
                total_static += widget.height

        # loop over children
        for widget in self._children:

            # change the size hint with margin if specified
            if widget.size_hint_x is not None:
                widget.width = widget.size_hint_x * float(
                    self.width - self.padding_x.sum()
                ) - widget.margin_x.sum()

            else:
                widget.margin_x = 0.5 * float(
                    self.width - self.padding_x.sum() - widget.width
                )

            # set the position according to padding and margin
            widget.x = self.x + self.padding_left + widget.margin_left
            widget.y = (
                self.y + self.padding_top + total + widget.margin_top
            )

            # change the size hint with margin if specified
            if widget.size_hint_y is not None:
                widget.height = widget.size_hint_y * float(
                    self.height - self.padding_y.sum() - total_static
                ) - widget.margin_y.sum()

            # add to the total children height the new widget and its margin
            total_min += widget.minHeight + widget.margin_y.sum()
            total += widget.height + widget.margin_y.sum()

            # set to the width of the larger widget
            self.changedWidth.deactivate()
            self.width = max(widget.width, self.width)
            self.minWidth = max(
                widget.minWidth + widget.margin_x.sum() +
                self.padding_x.sum(),
                self.minWidth,
            )
            self.changedWidth.activate()

        # deactivate signal to avoid a deep recursion
        self.changedHeight.deactivate()

        self.minHeight = total_min + self.padding_y.sum()
        self.height = total + self.padding_y.sum()

        # reactivate the signal
        self.changedHeight.activate()


class HorizontalLayout(Widget):

    def __init__(self, *args, **kwargs):

        super(HorizontalLayout, self).__init__(*args, **kwargs)

        # call the method when powition is updated
        self.changedPosition.connect(self._update)
        self.changedPadding.connect(self._update)
        self.changedWidth.connect(self._update)
        self.changedHeight.connect(self._update)

    def addWidget(self, widget):
        """
        Add a widget to the list of children performing a pre processing to
        give the correct vertical layout to widgets.
        """

        # call parent to add correctly widget
        super(HorizontalLayout, self).addWidget(widget)

        # update positions
        self._update()

        # connect the widget to the position updater
        widget.changedMargin(self._update)

    def _update(self, *args, **kwargs):
        """
        Connected to the signal emitted when the position of the container
        changed.
        """

        # init the total height of childrens
        total = 0.
        total_min = 0.
        total_static = 0.

        # compute total static size
        for widget in self._children:
            if widget.size_hint_x is None:
                total_static += widget.width

        # loop over children
        for widget in self._children:

            # change the size hint with margin if specified
            if widget.size_hint_y is not None:
                widget.height = widget.size_hint_y * float(
                    self.height - self.padding_y.sum()
                ) - widget.margin_y.sum()

            else:
                widget.margin_y = 0.5 * float(
                    self.height - self.padding_y.sum() - widget.height
                )

            # set the position according to padding and margin
            widget.y = self.y + self.padding_top + widget.margin_top
            widget.x = (
                self.x + self.padding_left + total + widget.margin_left
            )

            # change the size hint with margin if specified
            if widget.size_hint_x is not None:
                widget.width = widget.size_hint_x * float(
                    self.width - self.padding_x.sum() - total_static
                ) - widget.margin_x.sum()

            # add to the total children height the new widget and its margin
            total_min += widget.minWidth + widget.margin_x.sum()
            total += widget.width + widget.margin_x.sum()

            # set to the height of the larger widget
            self.changedHeight.deactivate()
            self.minHeight = max(
                widget.minHeight + widget.margin_y.sum() +
                self.padding_y.sum(),
                self.minHeight,
            )
            self.changedHeight.activate()

        # deactivate the signal to avoid infinite recursion
        self.changedWidth.deactivate()

        self.minWidth = total_min + self.padding_x.sum()
        self.width = total + self.padding_x.sum()

        # reactivate the signal to inform for changes
        self.changedWidth.activate()

# vim: set tw=79 :
