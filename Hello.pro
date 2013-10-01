#-------------------------------------------------
#
# Project created by QtCreator 2013-10-01T18:02:23
#
#-------------------------------------------------

QT       += core gui opengl

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = Hello
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    oglwidget.cpp

HEADERS  += mainwindow.h \
    oglwidget.hpp

FORMS    += mainwindow.ui
