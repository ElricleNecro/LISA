# -*- coding:Utf8 -*-

from OpenGL.arrays import numpymodule
from .OGLWidget import OGLWidget


numpymodule.NumpyHandler.ERROR_ON_COPY = True

__all__ = ["Figure"]


class Figure(object):

    def __init__(self, name="Figure {id:d}"):

        # set the window which will be the scene
        self.scene = OGLWidget("")
        self.scene.name = name.format(id=self.scene.id)

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        self._background_color = background_color

    def addWidget(self, wid):
        self.scene.addWidget(wid)

    def __getitem__(self, ind):
        return self.scene.lines[ind]

    def __delitem__(self, ind):
        pass

    @property
    def axes(self):
        return self.scene.lines

    @axes.setter
    def axes(self, value):

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

        # store the instance for plots
        self.scene.lines = value

    def close(self):
        self.scene.close()
