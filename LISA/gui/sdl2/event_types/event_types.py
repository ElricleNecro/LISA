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

    Simply call the method, defined by the Meta.event_method of the instance of
    thewrapped method, of window that have the focus, with the attribute of the
    instance defined by Meta.event_attribute.
    """
    def decorator(self, event):
        # execute the processing of the event
        func(self, event)

        # call the good method of the window with the focus
        if self.window.id in SDLWindow.manager.windowsById:
            # get the window with the focus
            window = SDLWindow.manager.windowsById[self.window.id]

            # check it has the method to call in the window
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
    A base class for the kind of SDL events to manage in the window. The
    keyword arguments given to the class are stored into the instance as
    attributes. So the typical use of the class is to set to it the structures
    handling the keyboard, mouse, wheel and window state. To be able to access
    them in the event instance.

    The class uses several meta informations stored into the class Meta in
    attribute, to be able to register easily the event class associated to an
    SDL event, and to communicate to the window.

    The Meta.register_type refers to the SDL event associated associated to the
    EventType class. Through the EventTypeMetaclass metaclass, when a class is
    derived from the EventType base class, the new class is automatically
    registered into the available_events attribute set by the metaclass. This
    is a mapping between the Meta.register_type and the class itself, allowing
    to handle events. Since derived EventType instances are singleton, we can
    also make a mapping between the Meta.register_type and the instance, stored
    in the events attribute.

    The Meta.event_method is the name of the method to call in the current
    window with the structure containing informations on the event. The current
    window is determined by the window with the current focus, actually given
    by SDL in the structure of the event. Since we have a window manager, we
    can easily access to it.

    The Meta.event_attribute is the attribute of the derived EventType
    instance, that will be given as argument to the method in the current
    window referenced by Meta.event_method.

    Then, all available events are instantiated by the event loop, and the
    keyboard, mouse, wheel and window structures are passed at the
    initialization and set as attributes.
    """
    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        """
        At the initialization, the keywords arguments are processed to be set
        as attributes of the event type, allowing to access some variables
        inside the event processing. The typical use is to set the keyboard,
        wheel, mouse and window structure containing informations about events.
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
        A method called to process the event. This method take the SDL event
        extracted from the PollEvent as an argument. The event is then
        processed by the processEvent method of the derived class of EventType,
        putting interesting informations to the keyboard, mouse, wheel and
        window structures.

        It is the eventor decorator that is responsible to give the good
        structure to the good method of the current window.
        """
        pass


class WindowEventType(object, metaclass=EventTypeMetaclass):
    """
    Base class for window events. The principle is the same as for EventType.
    This is just a new class since the way to handle it is not the same for
    window event, since the Meta.register_type key used for the mapping is not
    the same. Refer to EventType for details.
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
