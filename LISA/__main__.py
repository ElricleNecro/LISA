#! /usr/bin/env python
# -*- coding:Utf8 -*-

import sys
import numpy as np
import OGLWidget as og
import Figure as f

from PyQt5 import Qt
from PyQt5 import QtGui as qg
from OpenGL import GL
from OpenGL.arrays import numpymodule
from examples.rippler.rippler import Rippler
from examples.heightmap.heightmap import HeightMap

numpymodule.NumpyHandler.ERROR_ON_COPY = True




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
    fig.axes = Rippler()
    fig.axes = HeightMap()
    fig.show()

    sys.exit(app.exec_())
