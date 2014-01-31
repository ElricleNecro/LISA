#-------------------------------------------------
#
# Project created by QtCreator 2013-10-01T18:02:23
#
#-------------------------------------------------

QT       += core gui opengl

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CFLAGS += -g -std=c++11
CXXFLAGS += -g -std=c++11
TARGET = Hello
TEMPLATE = app
LIBS += -lGLU
INCLUDEPATH += include/

SOURCES += src/main.cpp\
	   src/oglwidget.cpp \
	   src/OGLCube.cpp \
	   src/gadget.cpp \

HEADERS  += include/oglwidget.hpp \
	    include/OGLCube.hpp \
	    include/gadget.hpp \
	    include/interface.hpp \

#include/mainwindow.h \
#src/mainwindow.cpp \
#

FORMS    += mainwindow.ui
