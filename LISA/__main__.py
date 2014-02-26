#! /usr/bin/env python
# -*- coding:Utf8 -*-

import sys
import numpy as np
import OGLWidget as og

from PyQt5 import Qt
from PyQt5 import QtGui as qg
from OpenGL import GL

class TestOGL(object):
	def __init__(self, *args, **kwargs):
		rand = np.random.rand(1000, 3)
		self._color = np.random.rand(1000, 3)

		r    = rand[:,0]**(1./3.)
		thet = np.arccos(2*rand[:,1] - 1)
		phi  = 2.*np.pi * rand[:,2]

		self._pos = np.array(
				[
					r*np.cos(phi)*np.sin(thet),
					r*np.sin(phi)*np.sin(thet),
					r*np.cos(thet)
				]
		).T

	def show(self, shaders, matrice):
		shaders.setUniformValue("modelview", matrice)

		shaders.setAttributeArray("in_Vertex", self._pos)
		shaders.setAttributeArray("in_Color", self._color)

		shaders.enableAttributeArray("in_Vertex")
		shaders.enableAttributeArray("in_Color")

		GL.glDrawArrays(GL.GL_POINTS, 0, self._pos.shape[0])

		shaders.disableAttributeArray("in_Vertex")
		shaders.disableAttributeArray("in_Color")

if __name__== "__main__":
	app = Qt.QApplication(sys.argv)

	aff = og.OGLWidget(TestOGL())
	aff.show()

	sys.exit( app.exec() )
