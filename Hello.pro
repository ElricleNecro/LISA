#-------------------------------------------------
#
# Project created by QtCreator 2013-10-01T18:02:23
#
#-------------------------------------------------

QT       += core gui opengl

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CFLAGS += -g
TARGET = Hello
TEMPLATE = app
LIBS += -lGLU
INCLUDEPATH += include/

SOURCES += src/main.cpp\
        src/mainwindow.cpp \
    src/oglwidget.cpp \
    src/OGLCube.cpp \

HEADERS  += include/mainwindow.h \
    include/oglwidget.hpp \
    include/OGLCube.hpp \

FORMS    += mainwindow.ui
