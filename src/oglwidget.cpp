#include "oglwidget.hpp"

OGLWidget::OGLWidget(QWidget *parent) : QGLWidget(parent), program(new QGLShaderProgram(this)), cube()
{

    projection.setToIdentity();
    modelview.setToIdentity();
    distance = 2.5;
    alpha = 25;
    beta = -25;
}

void OGLWidget::initializeGL()
{
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_CULL_FACE);

    qglClearColor(QColor(Qt::black));

    // Start by setting shaders
    program.removeAllShaders();
    program.addShaderFromSourceFile(QGLShader::Vertex, "Shaders/couleurs.vsh");
    program.addShaderFromSourceFile(QGLShader::Fragment, "Shaders/couleurs.fsh");

    // Activation du shader
    if( !program.link() )
    {
        std::cerr << "OGLCube.cpp:" << __LINE__ << " " << program.log().toStdString() << std::endl;
        throw std::runtime_error("Shader do not want to link");
    }
}

void OGLWidget::resizeGL( int width, int height )
{
    height = height?height:1;

    projection.setToIdentity();
    projection.perspective(60.0, (float)width/(float)height, 0.001, 1000);

    glViewport( 0, 0, width, height );
}

void OGLWidget::paintGL(void)
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    QMatrix4x4 mMatrix;
    QMatrix4x4 vMatrix;

    QMatrix4x4 cameraTransformation;
    cameraTransformation.rotate(alpha, 0, 1, 0);
    cameraTransformation.rotate(beta, 1, 0, 0);

    QVector3D cameraPosition = cameraTransformation * QVector3D(0, 0, this->distance);
    QVector3D cameraUpDirection = cameraTransformation * QVector3D(0, 1, 0);

    vMatrix.lookAt(cameraPosition, QVector3D(0, 0, 0), cameraUpDirection);

    program.bind();
    mMatrix = this->projection * vMatrix * mMatrix;

    this->cube.Show(this->program, mMatrix );

    program.release();
}

QSize OGLWidget::sizeHint() const
{
    return QSize(640, 480);
}

void OGLWidget::keyPressEvent( QKeyEvent *e )
{
    switch( e->key() )
    {
    case Qt::Key_Escape:
        close();
    }
}

void OGLWidget::mousePressEvent(QMouseEvent *event)
{
    lastMousePosition = event->pos();

    event->accept();
}

void OGLWidget::mouseMoveEvent(QMouseEvent *event)
{
    int deltaX = event->x() - lastMousePosition.x();
    int deltaY = event->y() - lastMousePosition.y();

    if (event->buttons() & Qt::LeftButton) {
        alpha -= deltaX;
        while (alpha < 0) {
            alpha += 360;
        }
        while (alpha >= 360) {
            alpha -= 360;
        }

        beta -= deltaY;
        if (beta < -90) {
            beta = -90;
        }
        if (beta > 90) {
            beta = 90;
        }

        updateGL();
    }

    lastMousePosition = event->pos();

    event->accept();
}

void OGLWidget::wheelEvent(QWheelEvent *event)
{
    int delta = event->delta();

    if (event->orientation() == Qt::Vertical) {
        if (delta < 0) {
            distance *= 1.1;
        } else if (delta > 0) {
            distance *= 0.9;
        }

        updateGL();
    }

    event->accept();
}
