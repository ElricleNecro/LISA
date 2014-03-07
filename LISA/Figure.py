# -*- coding:Utf8 -*-

import OGLWidget as og

from PyQt5 import Qt, QtOpenGL as qo, QtGui as qg, QtCore as qc


class Scene(Qt.QGraphicsScene):

    def __init__(self, EventHandler, *args, **kwargs):
        super(Scene, self).__init__(*args, **kwargs)
        self._event_handler = EventHandler
        self._timer = EventHandler.getTimer(self)

    def wheelEvent(self, event):
        if event.isAccepted():
            return
        self._event_handler.wheelEvent(self)
        self.update()

    def mousePressEvent(self, event):
        if event.isAccepted():
            return
        self._event_handler.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.isAccepted():
            return
        if event.buttons() == qc.Qt.LeftButton:
            self._event_handler.mouseMoveEvent(event)

        self.update()

    def mouseReleaseEvent(self, event):
        if event.isAccepted():
            return
        self._event_handler.mouseReleaseEvent(event)

    def timerEvent(self, event):
        self._event_handler.timerEvent(event)
        self.update()


class Figure(Qt.QGraphicsView):

    def __init__(self, *args, **kwargs):
        super(Figure, self).__init__(*args, **kwargs)

        # A color we need a lot of times:
        self._color = Qt.QColor()
        self._color.black()

        # Creation of the Plotting class:
        # Then we add it as background of the View:
        # self.setViewport(self._axes)
        context = qo.QGLWidget()
        self.setViewport(context)
        context.makeCurrent()
        self.setViewportUpdateMode(Qt.QGraphicsView.FullViewportUpdate)

        # And we set it as scene for the View:
        self._axes = og.OGLWidget()
        self._axes.createDialog()
        self.setScene(self._axes)
        self._axes.initializeGL()

        # Set some properties and palette to have a black background:
        self.setAutoFillBackground(True)
        self.setPalette(
            qg.QPalette(
                self._color
            )
        )
        context.doneCurrent()

    def resizeEvent(self, event):
        self._axes.resizeGL(event.size().width(), event.size().height())

    def keyPressEvent(self, event):
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

    def newWidget(self, wid):
        tmp = self._scene.addWidget(wid, qc.Qt.Window)
        tmp.setFlag(
            Qt.QGraphicsItem.ItemIsMovable
        )
        tmp.setCacheMode(
            Qt.QGraphicsItem.DeviceCoordinateCache
        )

    @property
    def axes(self):
        return self._axes.lines

    @axes.setter
    def axes(self, value):
        self._axes.lines = value

        try:
            wid = value.createWidget()
            if wid:
                self.newWidget(wid)
        except AttributeError:
            pass
