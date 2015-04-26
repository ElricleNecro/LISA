#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import logging

from ..window import SDLWindow

__all__ = ["EventType", "eventor", "WindowEventType"]

logger = logging.getLogger(__name__)


def eventor(func):
    """
    A decorator to indicate which method needs to be called after an event
    occurred. This allow to not process all the tree if no corresponding event
    happened.
    """
    def decorator(self, event):
        # execute the processing of the event
        func(self, event)

        # call the good method of the window with the focus
        if self.window.id in SDLWindow.manager.windowsById:
            # get the window with the focus
            window = SDLWindow.manager.windowsById[self.window.id]

            # check it has the method to call
            if hasattr(window, self.Meta.event_method):
                # call the method with the good event as argument
                getattr(window, self.Meta.event_method)(
                    getattr(self, self.Meta.event_attribute)
                )

    return decorator


class EventTypeMetaclass(abc.ABCMeta):
    """
    Metaclass to register available kinds of event type and easily access them
    without adding a lot of if statement in the code for each kind of event.
    """

    def __init__(cls, name, bases, attrs):
        # create the class as usual
        super(EventTypeMetaclass, cls).__init__(name, bases, attrs)

        # store the available classes
        if not hasattr(cls, "available_events"):
            cls.available_events = {}
        else:
            if not hasattr(cls.Meta, "register_type"):
                raise AttributeError(
                    "An event type needs meta attribute register_type"
                )
            cls.available_events[cls.Meta.register_type] = cls

        # mapping for instantiated events
        if not hasattr(cls, "events"):
            cls.events = {}

    def __call__(cls, *args, **kwargs):
        """
        Called when a class is instantiated.
        """
        # register the instance if not already created (events are singleton)
        if cls.Meta.register_type in cls.events:
            return cls.events[cls.Meta.register_type]

        # create the instance
        instance = super(EventTypeMetaclass, cls).__call__(*args, **kwargs)

        # store it to retrieve it later
        cls.events[instance.Meta.register_type] = instance

        return instance


class EventType(object, metaclass=EventTypeMetaclass):
    """
    A base class for the kind of SDL events to manage in the window.
    """
    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        """
        At the initialization, the keywords arguments are processed to be set
        as attributes of the event type, allowing to access some variables
        inside the event processing.
        """
        # check that no arguments are given
        if len(args):
            raise ValueError("Event type is initialized only with keywords")

        # for each keyword argument, store an attribute
        for key, value in kwargs.items():
            setattr(self, key, value)

    @eventor
    @abc.abstractmethod
    def processEvent(self, event):
        """
        A method called to process the event.
        """
        pass


class WindowEventType(object, metaclass=EventTypeMetaclass):
    """
    Base class for window events.
    """

    def __init__(self, *args, **kwargs):
        """
        At the initialization, the keywords arguments are processed to be set
        as attributes of the event type, allowing to access some variables
        inside the event processing.
        """
        # check that no arguments are given
        if len(args):
            raise ValueError(
                "Window event type is initialized only with keywords"
            )

        # for each keyword argument, store an attribute
        for key, value in kwargs.items():
            setattr(self, key, value)

    @eventor
    @abc.abstractmethod
    def processEvent(self, event):
        """
        A method called to process the event.
        """
        pass


# vim: set tw=79 :
