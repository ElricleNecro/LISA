#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .events import SDLInput
from .window import SDLWindow

import sdl2 as s

__all__ = ["EventLoop"]


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


class SDL2_Dealer(object, metaclass=EventLoopMetaclass):
    def __init__(self, fps=60):
        """
        Init SDL and connect to the signal sent by the window manager when a
        window is created to launch the event loop at this time.
        """
        # init SDL
        s.SDL_Init(s.SDL_INIT_VIDEO)

        self._ev = SDLInput()
        self._hook = None
        self.fps = fps
        self._in_event_loop = False

        # connect to added signal of the window manager
        SDLWindow.manager.created.connect(self.passEventLoop)

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


try:
    from IPython.lib.inputhook import InputHookManager, stdin_ready
    from IPython.lib.inputhook import allow_CTRL_C

    class EventLoop(SDL2_Dealer):
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
                self._ev.update()

                # loop over created windows to draw them
                for win in SDLWindow.manager.windows:
                    win.draw()

                # get the time after processing
                stop = s.SDL_GetTicks()

                # compute elapsed time in the frame
                duree = (stop - start)

                # if there is remaining time compared to the specified frame
                # rate, put the program in pause for the rest of the time
                if duree < self._framerate:
                    s.SDL_Delay(self._framerate - duree)


except:
    class EventLoop(SDL2_Dealer):
        def __init__(self, *args, **kwargs):
            super(EventLoop, self).__init__(*args, **kwargs)


eventLoop = EventLoop()


# vim: set tw=79 :
