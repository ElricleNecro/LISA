#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .events import SDLInput

import sdl2 as s


class SDL2_Dealer(object):
    def __init__(self, fps=60):
        s.SDL_Init(s.SDL_INIT_VIDEO)

        self._windowList = dict()
        self._ev = SDLInput()
        self._hook = None
        self._framerate = int(1000 / fps)
        self._in_event_loop = False

    def add(self, val):
        self._windowList[val.id] = val

    def erase(self, val):
        del self._windowList[val.id]

    def __del__(self):
        s.SDL_Quit()

try:
    from IPython.lib.inputhook import InputHookManager, stdin_ready
    from IPython.lib.inputhook import allow_CTRL_C

    class SDL2_Deal(SDL2_Dealer):
        def __init__(self, *args, **kwargs):

            super(SDL2_Deal, self).__init__(*args, **kwargs)
            self._hook = InputHookManager()
            self.launch_events()

        def launch_events(self):
            if not self._in_event_loop:
                self._in_event_loop = True

            def events():
                self._dealEvents()
                self._in_event_loop = False
                return 0

            self._hook.set_inputhook(events)

        def _dealEvents(self):
            allow_CTRL_C()
            while not stdin_ready():
                start = s.SDL_GetTicks()

                self._ev.update()

                if len(self._windowList):
                    if self._ev.window.id in self._windowList:
                        self._windowList[self._ev.window.id].events(self._ev)

                for win in self._windowList.values():
                    win.draw()

                stop = s.SDL_GetTicks()
                duree = (stop - start)
                if duree < self._framerate:
                    s.SDL_Delay(self._framerate - duree)

except:

    class SDL2_Deal(SDL2_Dealer):
        def __init__(self, *args, **kwargs):
            super(SDL2_Deal, self).__init__(*args, **kwargs)

_ipython_way_sdl2 = SDL2_Deal()

# vim: set tw=79 :
