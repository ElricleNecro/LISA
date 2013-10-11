#ifndef OGLWIDGET_HPP
#define OGLWIDGET_HPP

#include <GL3/gl3.h>
#include <GL/glu.h>

#include <QtOpenGL/QtOpenGL>
#include <QTimer>

#include "OGLCube.hpp"
#include "OGLCamera.hpp"
#include "OGLMatrice.hpp"

class OGLWidget : public QGLWidget
{
        Q_OBJECT
    public:
        explicit OGLWidget(int timerInterval=0, QWidget *parent = 0);
    virtual void updateGL(void);

    protected:
        virtual void initializeGL();
        virtual void resizeGL( int width, int height );
        virtual void paintGL();

        virtual void keyPressEvent( QKeyEvent *e );

        virtual void timeOut();

    signals:

    protected slots:
        virtual void timeOutSlot();

    private:
        QGLShaderProgram program;
        QTimer *m_timer;
        OGLCube::OGLCube cube;
        OGLCamera::OGLCamera camera;
        OGLMatrice::OGLMatrice projection, modelview;
        double angle, z;
};

#endif // OGLWIDGET_HPP
