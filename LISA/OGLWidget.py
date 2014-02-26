#! /usr/bin/env python
# -*- coding:Utf8 -*-

from PyQt5 import Qt, QtOpenGL as qo, QtGui as qg
from OpenGL import GL

class ShadersNotLinked(Exception):
	def __init__(self, msg):
		self._msg = msg

	def __str__(self):
		return self._msg

class OGLWidget(qo.QGLWidget):
	def __init__(self, *args, **kwargs):
		super(OGLWidget, self).__init__(*args, **kwargs)

		# Data class to plot:
		self._data               = []

		# Find how to use and implements those one:
		self._timer              = Qt.QBasicTimer()

		self._shaders            = qg.QOpenGLShaderProgram(self)

		# Different matrix use for the on screen printing:
		self._projection         = Qt.QMatrix4x4()
		self._projection.setToIdentity()
		self._model              = Qt.QMatrix4x4()
		self._model.setToIdentity()
		self._view               = Qt.QMatrix4x4()
		self._view.setToIdentity()
		self._camera             = Qt.QMatrix4x4()
		self._camera.setToIdentity()

		# Some variables use to parametrized printing:
		self._angularSpeed       = 0.0
		self._distance           = 1.0

		# Some variables use to keep track of what we are doing with events:
		self._lastMousePosition  = Qt.QPoint()
		self._rotate             = qg.QQuaternion()

		self._mousePressPosition = Qt.QVector2D()
		self._rotationAxis       = Qt.QVector3D()

	@property
	def lines(self):
		return self._data
	@lines.setter
	def lines(self, value):
		self._data.append(value)

	def initializeGL(self):
		print("initialiseGL")
		GL.glEnable(GL.GL_DEPTH_TEST)
		GL.glEnable(GL.GL_CULL_FACE)

		color = Qt.QColor()
		color.black()
		self.qglClearColor(color)

		self._shaders.removeAllShaders()
		self._shaders.addShaderFromSourceFile(qg.QOpenGLShader.Vertex,   "Shaders/couleurs.vsh")
		self._shaders.addShaderFromSourceFile(qg.QOpenGLShader.Fragment, "Shaders/couleurs.fsh")

		if not self._shaders.link():
			raise ShadersNotLinked("Linking shaders in OGLWidget.initialiseGL has failed! " + self._shaders.log())

		self._timer.start(12, self)

	def resizeGL(self, w, h):
		h = 1 if h == 0 else h

		self._projection.setToIdentity()
		self._projection.perspective(60.0, w/h, 0.001, 1000.0)

		GL.glViewport(0, 0, w, h)

	def paintGL(self):
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

		cam_pos = Qt.QVector3D(0, 0, self._distance)
		cam_up  = Qt.QVector3D(0, 1, 0)

		self._view.setToIdentity()

		self._view.lookAt(cam_pos, Qt.QVector3D(0, 0, 0), cam_up)

		self._view.rotate(self._rotate)

		self._shaders.bind()

		matrice = self._projection * self._view * self._model

		for data in self._data:
			data.show(self._shaders, matrice)

		self._shaders.release()

	def keyPressEvent(self, event):
		pass

	def wheelEvent(self, event):
		pass

	def mousePressEvent(self, event):
		pass

	def mouseReleaseEvent(self, event):
		pass

