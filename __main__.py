#! /usr/bin/env python
# -*- coding:Utf8 -*-

import sys

#from PyQt5 import Qt as q
from PyQt4 import QtGui as q
from OpenGL.arrays import numpymodule
from LISA.examples import Rippler
from LISA.examples import HeightMap
from LISA.examples import Sprites
from LISA import Figure

numpymodule.NumpyHandler.ERROR_ON_COPY = True


if __name__ == "__main__":
    app = q.QApplication(sys.argv)

    fig = Figure()
    fig.axes = Sprites()
    #fig.axes = Rippler()
    #fig.axes = HeightMap()
    fig.show()

    sys.exit(app.exec_())
