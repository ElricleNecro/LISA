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
        s.SDL_Init(s.SDL_INIT_VIDEO)

        self._ev = SDLInput()
        self._hook = None
        self._framerate = int(1000 / fps)
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


try:
    from IPython.lib.inputhook import InputHookManager, stdin_ready
    from IPython.lib.inputhook import allow_CTRL_C

    class EventLoop(SDL2_Dealer):
        def __init__(self, *args, **kwargs):
            super(EventLoop, self).__init__(*args, **kwargs)
            self._hook = InputHookManager()

        def launch_events(self):
            if not self._in_event_loop:
                self._in_event_loop = True

            def events():
                self._dealEvents()
                return 0

            self._hook.set_inputhook(events)

        def _dealEvents(self):
            allow_CTRL_C()
            while not stdin_ready():
                start = s.SDL_GetTicks()

                self._ev.update()

                for win in SDLWindow.manager.windows:
                    win.draw()

                stop = s.SDL_GetTicks()
                duree = (stop - start)
                if duree < self._framerate:
                    s.SDL_Delay(self._framerate - duree)


except:
    class EventLoop(SDL2_Dealer):
        def __init__(self, *args, **kwargs):
            super(EventLoop, self).__init__(*args, **kwargs)


eventLoop = EventLoop()


# vim: set tw=79 :
