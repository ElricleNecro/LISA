# -*- coding:Utf8 -*-

from PyQt5 import Qt
#from PyQt5 import QtOpenGL as qo
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
from OpenGL import GL
from OpenGL.arrays import numpymodule

numpymodule.NumpyHandler.ERROR_ON_COPY = True


class OGLWidget(Qt.QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super(OGLWidget, self).__init__(*args, **kwargs)

        # Data class to plot:
        self._data = []

        # Different matrix use for the on screen printing:
        self._projection = Qt.QMatrix4x4()
        self._projection.setToIdentity()
        self._model = Qt.QMatrix4x4()
        self._model.setToIdentity()
        self._view = Qt.QMatrix4x4()
        self._view.setToIdentity()
        self._camera = Qt.QMatrix4x4()
        self._camera.setToIdentity()

        # Some variables use to parametrized printing:
        self._angularSpeed = 0.0
        self._distance = 1.0

        # Some variables use to keep track of what we are doing with events:
        self._lastMousePosition = Qt.QPoint()
        self._rotate = qg.QQuaternion()

        self._mousePressPosition = False
        self._rotationAxis = Qt.QVector3D()

        self._timer = Qt.QBasicTimer()

    @property
    def lines(self):
        return self._data

    @lines.setter
    def lines(self, value):
        self._data.append(value)

    def initializeGL(self):

        self._timer.start(12, self)

    def resizeGL(self, w, h):
        h = 1 if h == 0 else h

        self._projection.setToIdentity()
        self._projection.perspective(60.0, w / h, 0.001, 1000.0)
        self._screensize = Qt.QVector2D(w, h)

    def drawBackground(self, *args):

        self._cam_pos = Qt.QVector3D(0, 0, self._distance)
        cam_up = Qt.QVector3D(0, 1, 0)

        self._view.setToIdentity()

        self._view.lookAt(self._cam_pos, Qt.QVector3D(0, 0, 0), cam_up)

        self._view.rotate(self._rotate)

        #matrice = self._projection * self._view * self._model

        for data in self._data:
            data.show(self)

    def keyPressEvent(self, event):
        super(OGLWidget, self).keyPressEvent(event)

    def wheelEvent(self, event):
        super(OGLWidget, self).wheelEvent(event)
        if event.isAccepted():
            return
        delta = event.delta()

        if event.orientation() == qc.Qt.Vertical:
            if delta < 0:
                self._distance *= 1.1
            elif delta > 0:
                self._distance *= 0.9
            event.accept()
            self.update()

    def mousePressEvent(self, event):
        super(OGLWidget, self).mousePressEvent(event)
        if event.isAccepted():
            return
        self._mousePressPosition = True
        event.accept()
        self.update()

    def mouseMoveEvent(self, event):
        super(OGLWidget, self).mouseMoveEvent(event)
        if event.isAccepted():
            return
        if self._mousePressPosition:
            diff = Qt.QVector2D(event.scenePos()) - \
                Qt.QVector2D(event.lastScenePos())
            n = Qt.QVector3D(diff.y(), diff.x(), 0.0).normalized()
            acc = diff.length()
            self._rotationAxis = (n * acc).normalized()
            self._angularSpeed = acc
            self._rotate = qg.QQuaternion.fromAxisAndAngle(
                self._rotationAxis,
                self._angularSpeed,
            ) * self._rotate
            event.accept()
            self.update()

    def mouseReleaseEvent(self, event):
        super(OGLWidget, self).mouseReleaseEvent(event)
        if event.isAccepted():
            return
        self._mousePressPosition = False
        event.accept()
        self.update()

    def timerEvent(self, event):
        super(OGLWidget, self).timerEvent(event)
        self._angularSpeed *= 0.99

        if self._angularSpeed < 0.01:
            self._angularSpeed = 0.0
        else:
            self._rotate = qg.QQuaternion.fromAxisAndAngle(
                self._rotationAxis,
                self._angularSpeed,
            ) * self._rotate
        event.accept()
        self.update()
