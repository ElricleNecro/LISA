# -*- coding:Utf8 -*-

import OGLWidget as og

from PyQt5 import Qt, QtOpenGL as qo, QtGui as qg, QtCore as qc
from OpenGL.arrays import numpymodule

numpymodule.NumpyHandler.ERROR_ON_COPY = True


class Figure(Qt.QGraphicsView):

    def __init__(self, *args, **kwargs):
        super(Figure, self).__init__(*args, **kwargs)

        # A color we need a lot of times:
        self._color = Qt.QColor()
        self._color.black()

        # Creation of the Plotting class:
        # Then we add it as background of the View:
        self._context = qo.QGLWidget(Qt.QGLFormat(Qt.QGL.NoAccumBuffer))
        self.setViewport(self._context)

        # create the context for Opengl
        self._context.makeCurrent()

        # And we set it as scene for the View:
        self._axes = og.OGLWidget()
        self.setScene(self._axes)
        self._axes.initializeGL()

        # Set some properties and palette to have a black background:
        self.setAutoFillBackground(True)
        self.setPalette(
            qg.QPalette(
                self._color
            )
        )

        # unset the context ???
        self._context.doneCurrent()

    def addWidget(self, wid):
        tmp = self.scene().addWidget(wid, qc.Qt.Window)
        tmp.setFlag(
            Qt.QGraphicsItem.ItemIsMovable
        )
        tmp.setFlag(
            Qt.QGraphicsItem.ItemIsSelectable
        )
        tmp.setCacheMode(
            Qt.QGraphicsItem.DeviceCoordinateCache
        )

    def resizeEvent(self, event):
        if self._axes:
            self._axes.resizeGL(event.size().width(), event.size().height())
            super(Figure, self).resizeEvent(event)

    def keyPressEvent(self, event):
        super(Figure, self).keyPressEvent(event)
        if (
            event.modifiers() == qc.Qt.ControlModifier and
            event.key() == qc.Qt.Key_W
        ) or event.key() == qc.Qt.Key_Escape:
            print("Quiting!")
            self.close()
        else:
            event.ignore()

    def __getitem__(self, ind):
        return self._axes.lines[ind]

    def __delitem__(self, ind):
        pass

    @property
    def axes(self):
        return self._axes.lines

    @axes.setter
    def axes(self, value):
        self._axes.lines = value
        try:
            wid = value.createWidget()
            if wid:
                self.addWidget(wid)
        except AttributeError:
            pass
