***********************
Extending LISA's events
***********************

We start by the implementation of the transformation of events from SDL to
LISA.

.. _convert_sdl_event:

Converting SDL's events
=======================

Converting an SDL event to a LISA event is internally called processing the
event. LISA provides a framework to process events easily and independently of
the underlying system.

The class *EventProcessor* is responsible to register an event and to
automatically process it according to the type of the SDL event. By subclassing
the *EventProcessor*, any kind of SDL events can be easily processed and
converted to LISA events.

Here is an example on how to define a processor for the mouse motion event of
SDL:

.. code-block:: python

    from LISA.gui.sdl2.processors.processor_types import EventProcessor
    from LISA.gui.sdl2.application_events import MouseEvent
    from LISA.gui.sdl2.application_events import MouseMotion


    class MouseMotionEvent(EventProcessor):
        """
        To manage mouse motion event.
        """
        class Meta:
            register_type = sdl2.SDL_MOUSEMOTION

        @staticmethod
        def processEvent(event):
            ev = MouseEvent(MouseMotion, None)
            ev.dx = event.motion.xrel
            ev.dy = event.motion.yrel
            ev.x = event.motion.x
            ev.y = event.motion.y
            ev.windowId = event.motion.windowID
            return ev

The *MouseMotionEvent* class is subclassing the *EventProcessor* class and
overrides some attributes and method to adapt the task to be done for the
processing.

Firstly, LISA needs to know for which kind of SDL events the processing must be
done. Such informations are called meta-informations used by the processor,
since not really necessary for the user, but essential for the process to take
effect. Such properties are stored into a class named *Meta*, attribute of the
*EventProcessor* class. Then the *register_type* stores the SDL event type, the
type returned by the *type* method of the SDL event. When LISA encounters an
SDL event of the type *SDL_MOUSEMOTION*, an instance of the *MouseMotionEvent*
(a singleton) will automatically be called to process the SDL event by calling
the *processEvent* with the SDL event as an argument. The *register_type*
attribute is essential, since it is this attribute which allows the LISA
framework to control the processors to call when polling from the SDL events.

The *processEvent* in this example is then transforming the data contained into
the SDL event to be stored into a LISA *MouseEvent* instance. This instance is
then used by LISA to manage the interactions with the user in a system
abstracted way (see the :ref:`application_events` for details on how to use the
events relative to LISA). *processEvent* must be overriden by any subclass of
the EventProcessor. This method must return an instance derived from
*ApplicationEvent*, used then by LISA to dispatch appropriately the events to
the various objects in the scene(s).

.. note::

    I think that this way of processing events for the SDL framework can be
    sufficiently improved to be completely independent of the SDL framework,
    and allow us to use other backends for the creation of windows, such as Qt,
    Gtk, etc... It should be nice to make it sufficiently abstract for this.

.. _create_application_events:

Create application events
=========================

This section shows how to create a new application an integrate it into LISA's
framework. Let explain an example:

.. code-block:: python

    from LISA.gui.sdl2.application_events.application_event import ApplicationEvent
    from LISA.gui.sdl2.application_events.types import MouseUp
    from LISA.gui.sdl2.application_events.types import MouseDown
    from LISA.gui.sdl2.application_events.types import MouseMotion

    HANDLERS = {
        MouseUp: "mouseReleaseEvent",
        MouseDown: "mousePressEvent",
        MouseMotion: "mouseMoveEvent",
    }


    class MouseEvent(ApplicationEvent):
        """
        Class to handle and store informations on the mouse events.
        """
        def __init__(self, type, button):
            super(MouseEvent, self).__init__(type)

            self.button = button
            self.x = 0
            self.y = 0
            self.dx = 0
            self.dy = 0

        @property
        def type(self):
            return self._type

        @type.setter
        def type(self, type):
            if not type:
                return
            if type in HANDLERS:
                self._type = type
                return

        @property
        def handler(self):
            return HANDLERS[self.type]


The event framework of LISA is strongly inspired by the one of the Qt
framework, so if you are familiar with it, you should see some common ideas in
the principle. We create a class for managing mouse events in each objects of
LISA. For this, the *MouseEvent* class must subclass the *ApplicationEvent*.
Each *ApplicationEvent* must be initialized with a given type, allowing a fine
tuning of the task to perform with this event. This is easily understandable
with mouse events, since there are several of them, such as motion, button
press or down, etc, which LISA must be able to handle.

At the initialization, the *MouseEvent* takes extra parameters for extra
informations, in this case the button implicated with event. It gives also
default values for attributes used by LISA, such as the position of the mouse
for the event (*x* and *y*), or the relative motion of the mouse in case of a
motion (*dx*, *dy*).

Here, the *type* property is overriden to check if the given type at the
construction is accepted by the class.

The *handler* property returns the name of the method to call on LISA scene
objects to handle the given application event. This method will be called with
the instance of the application event as argument. For example, if we construct
a *MouseEvent* with type *MouseUp*, the window with the focus will have its
*mouseReleaseEvent* method called by the framework with this *MouseEvent*
instance as argument.
