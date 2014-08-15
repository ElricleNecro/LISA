# -*- coding:Utf8 -*-

from OpenGL.arrays import numpymodule
from OpenGL import GL

from LISA.gui.utils.matrices import Perspective
from .window import SDLWindow

import LISA.Matrice as m

numpymodule.NumpyHandler.ERROR_ON_COPY = True


__all__ = ["OGLWidget"]


class OGLWidget(SDLWindow):

    def __init__(self, *args, **kwargs):

        # Data class to plot:
        self._data = []

        # Different matrix use for the on screen printing:
        self.projection = Perspective(shape=(4, 4), dtype="float32")
        self.model = m.Identity()
        self.view = m.Identity()
        self.camera = m.Identity()
        self.camera_up = m.Vector(0., 1., 0.)
        self.camera_target = m.Vector(0., 0., 0.)
        self.camera = m.Vector(0, 0, 1.)
        self.zoom = 1.0

        # Some variables use to keep track of what we are doing with events:
        self.rotate = m.Identity()

        self._mousePress = False

        super(OGLWidget, self).__init__(*args, **kwargs)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, zoom):
        self._zoom = zoom
        self.camera = (
            1 - self._zoom
        ) * self.camera_target + self._zoom * self.camera

    @property
    def projection(self):
        return self._projection

    @projection.setter
    def projection(self, projection):
        self._projection = projection

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, view):
        self._view = view

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, camera):
        self._camera = camera

    @property
    def camera_up(self):
        return self._camera_up

    @camera_up.setter
    def camera_up(self, camera_up):
        self._camera_up = camera_up

    @property
    def camera_target(self):
        return self._camera_target

    @camera_target.setter
    def camera_target(self, camera_target):
        self._camera_target = camera_target

    @property
    def rotate(self):
        return self._rotate

    @rotate.setter
    def rotate(self, rotate):
        self._rotate = rotate

    @property
    def lines(self):
        return self._data

    @lines.setter
    def lines(self, value):
        self._data.append(value)

    def resizeGL(self, w, h):
        h = 1 if h == 0 else h
        self.projection.ratio = w / h
        self._screensize = m.Vector(w, h)

    def draw(self, *args):

        self.view.setToIdentity()

        self.view.lookAt(
            self.camera,
            self.camera_target,
            self.camera_up,
        )

        self.view *= self.rotate

        self.makeCurrent()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        for data in self._data:
            data.show(self)

        self.update()

    def keyPressEvent(self, event):
        # super(OGLWidget, self).keyPressEvent(event)
        pass

    def wheelEvent(self, event):
        super(OGLWidget, self).wheelEvent(event)
        # if event.isAccepted():
        # return
        delta = event._y_wheel

        # if event.orientation() == Qt.Vertical:
        if delta < 0:
            self.zoom = 1.15
        elif delta > 0:
            self.zoom = 0.87
        # event.accept()
        # self.update()

    def mousePressEvent(self, event):
        super(OGLWidget, self).mousePressEvent(event)
        self._mousePress = True

    def mouseMoveEvent(self, event):
        super(OGLWidget, self).mouseMoveEvent(event)
        if self._mousePress:

            # compute the movement of the mouse
            x, y = event._xRel, event._yRel

            # if no movement, do nothing
            if x == 0 and y == 0:
                return

            # create the rotation axis
            rotationAxis = m.Vector(y, x, 0.0)

            # make the angular speed to its norm
            angularSpeed = rotationAxis.norm()

            # create the quaternion matrix and apply it to the last state
            self.rotate = m.Translation(self.camera_target) * m.Quaternion(
                angularSpeed,
                rotationAxis
            ) * m.Translation(-self.camera_target) * self.rotate

    def mouseReleaseEvent(self, event):
        super(OGLWidget, self).mouseReleaseEvent(event)
        self._mousePress = False

# vim: set tw=79 :
