#ifndef OGLWIDGET_HPP
#define OGLWIDGET_HPP

#include <GL3/gl3.h>
#include <GL/glu.h>

#include <QtOpenGL/QtOpenGL>
#include <QTimer>

#include <iostream>
#include "OGLCube.hpp"

class OGLWidget : public QGLWidget
{
        Q_OBJECT
    public:
        OGLWidget(QWidget *parent = 0);
        QSize sizeHint() const;

    protected:
        virtual void initializeGL();
        virtual void resizeGL( int width, int height );
        virtual void paintGL();

        virtual void keyPressEvent( QKeyEvent *e );
        virtual void mouseMoveEvent(QMouseEvent *event);
        virtual void wheelEvent(QWheelEvent *event);
        virtual void mousePressEvent(QMouseEvent *event);

    private:
        QGLShaderProgram program;
        QTimer *m_timer;
        OGLCube::OGLCube cube;
        QMatrix4x4 camera;
        QMatrix4x4 projection, modelview;
        QPoint lastMousePosition;
        double angle;
        double alpha;
        double beta;
        double distance;
};

#endif // OGLWIDGET_HPP
