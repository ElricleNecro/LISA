# -*- coding:Utf8 -*-

from OpenGL.arrays import numpymodule

from LISA import Matrice as m
from .window import SDLWindow

import math as mm

numpymodule.NumpyHandler.ERROR_ON_COPY = True


class OGLWidget(SDLWindow):

    def __init__(self, *args, **kwargs):
        super(OGLWidget, self).__init__(*args, **kwargs)

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
        # delta = event.delta()

        # if event.orientation() == Qt.Vertical:
        # if delta < 0:
        # self.zoom = 1.15
        # elif delta > 0:
        # self.zoom = 0.87
        # event.accept()
        # self.update()

    def mousePressEvent(self, event):
        super(OGLWidget, self).mousePressEvent(event)
        if event.isAccepted():
            return
        self._mousePress = True
        event.accept()
        self.update()

    def mouseMoveEvent(self, event):
        super(OGLWidget, self).mouseMoveEvent(event)
        if event.isAccepted():
            return
        if self._mousePress:

            # get event for the current position and last one
            new, last = event.scenePos(), event.lastScenePos()

            # compute the movement of the mouse
            x, y = new.x() - last.x(), new.y() - last.y()

            # if no movement, do nothing
            if x == 0 and y == 0:
                event.accept()
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

            # handle event
            event.accept()
            self.update()

    def mouseReleaseEvent(self, event):
        super(OGLWidget, self).mouseReleaseEvent(event)
        if event.isAccepted():
            return
        self._mousePress = False
        event.accept()
        self.update()


class Perspective(m.Matrix):

    def __init__(self, *args, **kwargs):
        super(Perspective, self).__init__(*args, **kwargs)

        self._angle = 60.0
        self._ratio = 16 / 9
        self._minimal = 0.000001
        self._maximal = 10000000.0
        self._setf()
        self[:] = m.Perspective(
            self._angle,
            self._ratio,
            self._minimal,
            self._maximal,
        )[:]

    def _setf(self):
        self._f = 1. / mm.tan(self._angle / 2.0 * mm.pi / 180.)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self._setf()
        self[0, 0] = self._f / self._ratio
        self[1, 1] = self._f

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, ratio):
        self._ratio = ratio
        self[0, 0] = self._f / self._ratio

    @property
    def minimal(self):
        return self._minimal

    @minimal.setter
    def minimal(self, minimal):
        self._minimal = minimal
        self[2, 2] = (
            self._minimal + self._maximal
        ) / (self._minimal - self._maximal)
        self[2, 3] = 2. * self._minimal * self._maximal / (
            self._minimal - self._maximal
        )

    @property
    def maximal(self):
        return self._maximal

    @maximal.setter
    def maximal(self, maximal):
        self._maximal = maximal
        self[2, 2] = (
            self._minimal + self._maximal
        ) / (self._minimal - self._maximal)
        self[2, 3] = 2. * self._minimal * self._maximal / (
            self._minimal - self._maximal
        )
