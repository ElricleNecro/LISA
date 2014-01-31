#include "mainwindow.h"
#include "oglwidget.hpp"
#include "gadget.hpp"

#include <QApplication>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);

	Gadget obj("None_000");
	OGLWidget w(&obj);
	w.show();
	//x.show();

	return a.exec();
}
