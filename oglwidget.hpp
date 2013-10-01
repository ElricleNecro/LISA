#ifndef OGLWIDGET_HPP
#define OGLWIDGET_HPP

#include <QtOpenGL/QtOpenGL>

class OGLWidget : public QGLWidget
{
        Q_OBJECT
    public:
        explicit OGLWidget(QWidget *parent = 0);

    signals:

    public slots:

};

#endif // OGLWIDGET_HPP
