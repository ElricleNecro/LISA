#! /usr/bin/env python
# -*- coding:Utf8 -*-

import sys
import numpy as np
import OGLWidget as og
import Figure as f

from PyQt5 import Qt
from OpenGL import GL
from OpenGL.arrays import numpymodule
from OpenGL import contextdata

numpymodule.NumpyHandler.ERROR_ON_COPY = True


def cleanupCallback(context=None):
    """
    Create a cleanup callback to clear context-specific storage for the
    current context.
    """

    def callback(context=contextdata.getContext(context)):
        """
        Clean up the context, assumes that the context will *not* render again!
        """
        contextdata.cleanupContext(context)

    return callback


class TestOGL(object):

    def __init__(self, *args, **kwargs):
        rand = np.random.rand(1000, 3)
        self._color = np.random.rand(1000, 3)

        r = rand[:, 0] ** (1. / 3.)
        thet = np.arccos(2 * rand[:, 1] - 1)
        phi = 2. * np.pi * rand[:, 2]

        self._pos = np.array(
            [
                r * np.cos(phi) * np.sin(thet),
                r * np.sin(phi) * np.sin(thet),
                r * np.cos(thet)
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

    def createWidget(self, title="Dialogue de test.", parent=None):
        dialog = Qt.QDialog(parent=parent)
        dialog.setWindowOpacity(0.4)
        dialog.setWindowTitle(title)
        dialog.setLayout(Qt.QVBoxLayout())
        dialog.layout().addWidget(
            Qt.QLabel("Ceci est un test d'affichage des widgets.")
        )
        dialog.layout().addWidget(
            Qt.QLabel("Ceci est un test d'affichage des widgets.")
        )
        but = Qt.QPushButton()
        but.setText("Un bouton !")
        but.clicked.connect(self._push_button)
        dialog.layout().addWidget(but)

        return dialog

    def _push_button(self):
        pass


def testOGLWidget():
    app = Qt.QApplication(sys.argv)

    aff = og.OGLWidget()
    for i in range(3):
        aff.lines = TestOGL()
    aff.show()

    return app.exec_()


def testFigure():
    app = Qt.QApplication(sys.argv)

    fig = f.Figure()
    fig.axes = TestOGL()
    fig.show()

    return app.exec_()


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)

    fig = f.Figure()
    fig.axes = TestOGL()
    fig.show()

    sys.exit(app.exec_())
