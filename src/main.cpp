#include "mainwindow.h"
#include "oglwidget.hpp"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);


    OGLWidget w, x;
    w.show();
    //x.show();

    return a.exec();
}
