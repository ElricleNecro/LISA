#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path as osp
import collections
import logging.config
import logging
import ctypes
import json
import os

from .window import SDLWindow
from .processors import EventProcessor
from ...tools import config_path

import sdl2 as s

__all__ = ["EventLoop"]

logger = logging.getLogger(__name__)

def setLogger():
    """
    Create a logger with the correct name for the module in order to see what
    happens in the program in different handlers (console, console in GUI,
    activity file, etc).
    """
    # get the path from where to read the configuration file for the platform
    # set default path
    path = config_path("logger.json")

    # get an environment variable for setting the configuration file for the
    # logger manually
    value = os.getenv("LISA_LOGGER_FILE", None)
    if value:
        path = value

    # standard verification for the file
    if osp.exists(path):
        # open the file and read its structure in json
        with open(path, 'rt') as f:
            config = json.load(f, object_pairs_hook=collections.OrderedDict)

        # set parameters to logging
        logging.config.dictConfig(config)
    else:
        raise ValueError(
            "The configuration file for the logger {0} doesn't exist".format(
                path
            )
        )


class EventLoopMetaclass(type):
    """
    Make the event loop a singleton.
    """
    def __call__(cls, *args, **kwargs):
        """
        Singleton for the event loop.
        """
        if hasattr(cls, "instance"):
            return cls.instance

        cls.instance = super(EventLoopMetaclass, cls).__call__(*args, **kwargs)
        return cls.instance


class BaseEventLoop(object, metaclass=EventLoopMetaclass):
    def __init__(self, fps=60):
        """
        Init SDL and connect to the signal sent by the window manager when a
        window is created to launch the event loop at this time.
        """
        # init SDL
        s.SDL_Init(s.SDL_INIT_VIDEO)

        # set fps
        self.fps = fps
        self._in_event_loop = False

        # connect to added signal of the window manager
        SDLWindow.manager.created.connect(self.passEventLoop)

        # create the queue for application events
        self.queue = collections.deque()

        # SDL event managers
        self._event = s.SDL_Event()

    def updateApplication(self):
        """
        Process the events from the queue for the application.
        """
        # clear the queue and send the events
        while(len(self.queue)):
            # get the event and receiver from the queue
            widget, event = self.queue.popleft()

            # send the event to the widget
            self.sendEvent(widget, event)

    def updateSDL(self):
        """
        Process the events from the system, given by SDL.
        """
        # loop over event in the queue
        while s.SDL_PollEvent(ctypes.byref(self._event)) != 0:
            # call the good event processor instance, by getting it from the
            # mapping in the manager
            if self._event.type in EventProcessor.manager:
                # process the SDL event with the good type
                event = EventProcessor.manager[self._event.type].processEvent(
                    self._event
                )

                # check that the event is handled
                if not event:
                    return

                # call the good method of the window with the focus
                if event.windowId in SDLWindow.manager.windowsById:
                    # get the window with the focus
                    window = SDLWindow.manager.windowsById[event.windowId]

                    # send the event in the queue of the application
                    self.postEvent(window, event)

    def update(self):
        """
        Process the events coming from the system and from the application.
        """
        # process what is coming from the application
        self.updateApplication()

        # process what is coming from the system
        self.updateSDL()

        # treat again the application since the system send things to the queue
        self.updateApplication()

    def passEventLoop(self, window):
        """
        Start the event loop when a window is created.
        """
        # start the event loop if not already launched
        self.launch_events()

    def launch_events(self):
        pass

    def __del__(self):
        s.SDL_Quit()

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps):
        self._fps = fps
        self._framerate = int(1000 / fps)

    def postEvent(self, receiver, event):
        """
        Post an event in the queue.
        """
        logger.debug("Posting {0} for {1}".format(event, receiver))
        self.queue.append((receiver, event))

    def sendEvent(self, receiver, event):
        # call the event handler of the widget
        logger.debug("Sending {0} to {1}".format(event, receiver))
        getattr(receiver, event.handler)(event)


try:
    from IPython.lib.inputhook import InputHookManager, stdin_ready
    from IPython.lib.inputhook import allow_CTRL_C

    class EventLoop(BaseEventLoop):
        def __init__(self, *args, **kwargs):
            super(EventLoop, self).__init__(*args, **kwargs)
            self._hook = InputHookManager()

        def launch_events(self):
            # check that the event loop is not already running
            if not self._in_event_loop:
                self._in_event_loop = True

            # define the function
            def events():
                self._dealEvents()
                return 0

            self._hook.set_inputhook(events)

        def _dealEvents(self):
            """
            Run the event loop at the framerate specified by the fps property
            of the event loop, and draw windows.
            """
            allow_CTRL_C()
            # run the event loop while the input is ready
            while not stdin_ready():
                # get the time at the start of the frame
                start = s.SDL_GetTicks()

                # process events in the event queue and dispatch them to the
                # windows
                self.update()

                # get the time after processing
                stop = s.SDL_GetTicks()

                # compute elapsed time in the frame
                duree = (stop - start)

                # if there is remaining time compared to the specified frame
                # rate, put the program in pause for the rest of the time
                if duree < self._framerate:
                    s.SDL_Delay(self._framerate - duree)


except:
    class EventLoop(BaseEventLoop):
        def __init__(self, *args, **kwargs):
            super(EventLoop, self).__init__(*args, **kwargs)


setLogger()

eventLoop = EventLoop()


# vim: set tw=79 :
