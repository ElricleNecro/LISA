#include "oglwidget.hpp"

OGLWidget::OGLWidget(int timerInterval, QWidget *parent) : QGLWidget(parent), program(parent), cube(), camera(0, 0, 2, 0, 0, 0, 0, 1, 0, 0.1, 0.6), projection(), modelview(), angle(0.0), z(2.0)
{
    if( timerInterval == 0 )
        m_timer = 0;
    else
    {
        m_timer = new QTimer( this );
        connect( m_timer, SIGNAL(timeout()), this, SLOT(timeOutSlot()) );
        m_timer->start( timerInterval );
    }

    projection.LoadIdentity();
    modelview.LoadIdentity();
}

void OGLWidget::initializeGL()
{
    glEnable(GL_DEPTH_TEST);
}

void OGLWidget::resizeGL( int width, int height )
{
    height = height?height:1;

    glViewport( 0, 0, (GLint)width, (GLint)height );

    projection.LoadIdentity();
    projection.LoadPerspective(70.0, (double)(width)/height, 1.0, 100.0);
}

void OGLWidget::paintGL(void)
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    this->updateGL();

    this->angle += 4.0;
    if( this->angle >= 360.0)
        this->angle = 0.0;
}

void OGLWidget::updateGL(void)
{
    this->modelview.LoadIdentity();
    this->modelview.LookAt(0, 0, this->z, 0, 0, 0, 0, 1, 0);
    this->camera.LookAt(modelview);
    this->modelview.Rotate(this->angle, 0, 1, 0);

    this->cube.Show(this->program, this->projection, this->modelview);
}

void OGLWidget::keyPressEvent( QKeyEvent *e )
{
    switch( e->key() )
    {
    case Qt::Key_Escape:
        close();
    }
}

void OGLWidget::timeOut()
{
}

void OGLWidget::timeOutSlot()
{
    timeOut();
}
