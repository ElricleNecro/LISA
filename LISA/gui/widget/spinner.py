#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .layout import HorizontalLayout, VerticalLayout
from .fonts import Text
from .button import Button
from LISA.gui.utils.signals import Signal


__all__ = ["Spinner"]


class Spinner(HorizontalLayout):

    def __init__(self, *args, **kwargs):

        # call the parent to be set correctly
        super(Spinner, self).__init__(*args, **kwargs)

        # say it can't expand
        self.size_hint = None

        # create a font object
        self.text = Text()
        self.text.size_hint = None

        # add it to the spinner layout
        self.addWidget(self.text)

        # create a vertical layout for buttons
        self.layout = VerticalLayout()
        self.layout.size_hint = None

        # create buttons plus
        self.plusButton = Button()
        self.plusButton.font_size = 15
        self.plusButton.text = "+"
        self.plusButton.size_hint = None
        self.plusButton.click.connect(self._add)

        # add it to vertical layout
        self.layout.addWidget(self.plusButton)

        # create buttons minus
        self.minusButton = Button()
        self.minusButton.font_size = 15
        self.minusButton.text = "-"
        self.minusButton.size_hint = None
        self.minusButton.click.connect(self._substract)

        # add it to vertical layout
        self.layout.addWidget(self.minusButton)

        # add the layout to the spinner
        self.addWidget(self.layout)

        # create a signal when the current value as changed
        self.changedCurrentValue = Signal()

        # set a default step
        self.step = 1
        self.currentValue = 0

    def _add(self, *args):
        self.currentValue += self.step

    def _substract(self, *args):
        self.currentValue -= self.step

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step):
        self._step = step
        if isinstance(self._step, int):
            self._format = "{0:d}"
        elif isinstance(self._step, float):
            self._format = "{0:.2f}"

    @property
    def currentValue(self):
        return self._currentValue

    @currentValue.setter
    def currentValue(self, currentValue):
        self._currentValue = currentValue
        text = self._format.format(self.currentValue)
        self.text.text = text
        self.changedCurrentValue(self._currentValue)

# vim: set tw=79 :
