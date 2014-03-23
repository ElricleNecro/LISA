# -*- coding:Utf8 -*-

#from PyQt5.Qt import *
#from PyQt5.QtOpenGL import *
#from PyQt5.QtGui import *
#from PyQt5.QtCore import *
from PyQt4.Qt import *
from PyQt4.QtOpenGL import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from OpenGL.arrays import numpymodule
from LISA.OGLWidget import OGLWidget
from IPython.lib import guisupport as gui
from IPython.lib.inputhook import InputHookManager

numpymodule.NumpyHandler.ERROR_ON_COPY = True

# create class managing hook for event loop in ipython
hook = InputHookManager()

# get the QApplication, creating one if not existing
app = gui.get_app_qt4()

# add the application to the hook
hook.enable_qt4(app)

# if event loop not running, run it for ipython
if not gui.is_event_loop_running_qt4(app):
    gui.start_event_loop_qt4(app)


class Figure(QGraphicsView):

    def __init__(self, *args, **kwargs):

        super(Figure, self).__init__(*args, **kwargs)

        # A color we need a lot of times:
        self._color = QColor()
        self._color.black()

        # Creation of the Plotting class:
        # Then we add it as background of the View:
        self._context = QGLWidget(QGLFormat(QGL.NoAccumBuffer))
        self.setViewport(self._context)

        # create the context for Opengl
        self._context.makeCurrent()

        # And we set it as scene for the View:
        self._axes = OGLWidget()
        self.setScene(self._axes)
        self._axes.initializeGL()

        # Set some properties and palette to have a black background:
        self.setAutoFillBackground(True)
        self.setPalette(
            QPalette(
                self._color
            )
        )

        # unset the context ???
        self._context.doneCurrent()

    def addWidget(self, wid):
        tmp = self.scene().addWidget(wid, Qt.Window)
        tmp.setFlag(
            QGraphicsItem.ItemIsMovable
        )
        tmp.setFlag(
            QGraphicsItem.ItemIsSelectable
        )
        tmp.setCacheMode(
            QGraphicsItem.DeviceCoordinateCache
        )

    def resizeEvent(self, event):
        if self._axes:
            self._axes.resizeGL(event.size().width(), event.size().height())
            super(Figure, self).resizeEvent(event)

    def keyPressEvent(self, event):
        super(Figure, self).keyPressEvent(event)
        if (
            event.modifiers() == Qt.ControlModifier and
            event.key() == Qt.Key_W
        ) or event.key() == Qt.Key_Escape:
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

        # store the instance for plots
        self._axes.lines = value

        # create shaders if there is one
        self._context.makeCurrent()
        try:
            value.createShaders(self._context)
        except AttributeError:
            pass
        self._context.doneCurrent()

        # add widget created by user
        try:
            wid = value.createWidget()
            if wid:
                self.addWidget(wid)
        except AttributeError:
            pass
