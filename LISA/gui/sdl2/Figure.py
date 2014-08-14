# -*- coding:Utf8 -*-

from OpenGL.arrays import numpymodule
from .events import SDLInput

import sdl2 as s


numpymodule.NumpyHandler.ERROR_ON_COPY = True


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
                return 0

            self._hook.set_inputhook(events)

        def _dealEvents(self):
            while not stdin_ready():
                start = s.SDL_GetTicks()

                self._ev.update()

                for win in self._windowList.values():
                    win.events(self._ev)
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


from .OGLWidget import OGLWidget


class Figure(object):

    def __init__(self, *args, **kwargs):

        # set the window which will be the scene
        self.scene = OGLWidget("Hello world")

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        self._background_color = background_color

    def addWidget(self, wid):
        pass

    def resizeEvent(self, event):
        if self.scene:
            self.scene.resizeGL(event.size().width(), event.size().height())
            super(Figure, self).resizeEvent(event)

    def __getitem__(self, ind):
        return self.scene.lines[ind]

    def __delitem__(self, ind):
        pass

    @property
    def axes(self):
        return self.scene.lines

    @axes.setter
    def axes(self, value):

        # store the instance for plots
        self.scene.lines = value

        # create shaders if there is one
        self.scene.makeCurrent()
        try:
            value.createShaders(self.scene)
        except AttributeError:
            pass

        # add widget created by user
        try:
            wid = value.createWidget()
            if wid:
                self.addWidget(wid)
        except:
            pass

    def close(self):
        self.scene.close()
