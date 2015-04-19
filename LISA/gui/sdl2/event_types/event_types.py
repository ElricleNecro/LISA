#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc

__all__ = ["EventType", "eventor"]


def eventor(func):
    """
    A decorator to indicate which method needs to be called after an event
    occurred. This allow to not process all the tree if no corresponding event
    happened.
    """
    def decorator(self, event):
        func(self, event)
        self.methods[self.__event_method__][0] = True
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
            if not hasattr(cls, "__register_type__"):
                raise AttributeError(
                    "An event type needs attribute __register_type__"
                )
            cls.available_events[cls.__register_type__] = cls

        # mapping for instantiated events
        if not hasattr(cls, "events"):
            cls.events = {}

    def __call__(cls, *args, **kwargs):
        """
        Called when a class is instantiated.
        """
        # register the instance if not already created (events are singleton)
        if cls.__register_type__ in cls.events:
            return cls.events[cls.__register_type__]

        # create the instance
        instance = super(EventTypeMetaclass, cls).__call__(*args, **kwargs)

        # store it to retrieve it later
        cls.events[instance.__register_type__] = instance

        return instance


class EventType(object, metaclass=EventTypeMetaclass):
    """
    A base class for the kind of SDL events to manage in the window.
    """

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


# vim: set tw=79 :
