#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

__all__ = ["EventProcessor", "WindowEventProcessor"]

logger = logging.getLogger(__name__)


class EventProcessorManager(object):
    """
    Class to manage the defined processors of the system events, register them
    access them easily.
    """
    def __init__(self):
        """
        Create containers.
        """
        self.processors = {}
        self.processorInstances = {}

    def add(self, cls):
        """
        Register a defined processor event.
        """
        if not hasattr(cls.Meta, "register_type"):
            logger.error("An event type needs meta attribute register_type")
            raise AttributeError(
                "An event type needs meta attribute register_type"
            )
            return

        self.processors[cls.Meta.register_type] = cls

    def __getitem__(self, kind):
        """
        Return an instance from the manager given the type of SDL event.
        """
        # get the instance processor
        if kind in self:
            return self.processors[kind]

    def __contains__(self, kind):
        return kind in self.processors


class EventProcessorMetaclass(type):
    """
    Metaclass to register available kinds of event type and easily access them
    without adding a lot of if statement in the code for each kind of event.
    """
    def __init__(cls, name, bases, attrs):
        # create the class as usual
        super(EventProcessorMetaclass, cls).__init__(name, bases, attrs)

        # store the available classes
        if not hasattr(cls, "manager"):
            cls.manager = EventProcessorManager()
            return

        # register the event processor
        cls.manager.add(cls)


class EventProcessor(object, metaclass=EventProcessorMetaclass):
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
    EventProcessor class. Through the EventProcessorMetaclass metaclass, when a class is
    derived from the EventProcessor base class, the new class is automatically
    registered into the available_events attribute set by the metaclass. This
    is a mapping between the Meta.register_type and the class itself, allowing
    to handle events. Since derived EventProcessor instances are singleton, we can
    also make a mapping between the Meta.register_type and the instance, stored
    in the events attribute.

    The Meta.event_method is the name of the method to call in the current
    window with the structure containing informations on the event. The current
    window is determined by the window with the current focus, actually given
    by SDL in the structure of the event. Since we have a window manager, we
    can easily access to it.

    The Meta.event_attribute is the attribute of the derived EventProcessor
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

    @staticmethod
    def processEvent(event):
        """
        A method called to process the event. This method take the SDL event
        extracted from the PollEvent as an argument. The event is then
        processed by the processEvent method of the derived class of
        EventProcessor, putting interesting informations to the keyboard,
        mouse, wheel and window structures. Then returns the good instance of
        the ApplicationEvent.
        """
        pass


class WindowEventProcessor(object, metaclass=EventProcessorMetaclass):
    """
    Base class for window events. The principle is the same as for EventProcessor.
    This is just a new class since the way to handle it is not the same for
    window event, since the Meta.register_type key used for the mapping is not
    the same. Refer to EventProcessor for details.
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

    @staticmethod
    def processEvent(event):
        """
        A method called to process the event.
        """
        pass


# vim: set tw=79 :
