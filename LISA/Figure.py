# -*- coding:Utf8 -*-

import OGLWidget as og

from PyQt5 import Qt, QtOpenGL as qo, QtGui as qg

class Figure(Qt.QGraphicsView):
	def __init__(self, *args, **kwargs):
		super(Figure, self).__init__(*args, **kwargs)

		# A color we need a lot of times:
		self._color = Qt.QColor()
		self._color.black()

		# Creation of the Plotting class:
		self._axes  = og.OGLWidget()
		# Then we add it as background of the View:
		self.setViewport(self._axes)
		self.setViewportUpdateMode(Qt.QGraphicsView.FullViewportUpdate)

		# We create the scene object which will contain all widget:
		self._scene = Qt.QGraphicsScene()
		# And we set it as scene for the View:
		self.setScene(self._scene)

		# Set some properties and palette to have a black background:
		self.setAutoFillBackground(True)
		self.setPalette(
				qg.QPalette(
					self._color
				)
		)

	def setupViewport(self, viewport):
		viewport.makeCurrent()
		self._axes.initializeGL()
		viewport.doneCurrent()

	def resizeEvent(self, event):
		print("resizeEvent")
		self._axes.resizeGL(event.size().width(), event.size().height())

	def drawBackground(self, painter, rect):
		print("drawBackground")
		self._axes.paintGL()

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
				self._scene.addWidget(wid)
		except AttributeError:
			pass
