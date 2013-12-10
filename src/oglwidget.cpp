#include "oglwidget.hpp"

OGLWidget::OGLWidget(QWidget *parent) : QGLWidget(parent), program(new QGLShaderProgram(this)), cube()
{

    this->projection.setToIdentity();
    this->modelview.setToIdentity();
    this->distance = 2.5;
    this->angularSpeed = 0.0;
    this->timer = new QBasicTimer();
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
    // using QBasicTimer because its faster that QTimer
    this->timer->start(12, this);
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

    QVector3D cameraPosition = cameraTransformation * QVector3D(0, 0, this->distance);
    QVector3D cameraUpDirection = cameraTransformation * QVector3D(0, 1, 0);

    vMatrix.lookAt(cameraPosition, QVector3D(0, 0, 0), cameraUpDirection);
    vMatrix.rotate(this->rotation);

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
    // Saving mouse press position
    this->mousePressPosition = QVector2D(event->localPos());
}

void OGLWidget::mouseMoveEvent(QMouseEvent *e)
{
    // Mouse release position - mouse press position
    QVector2D diff = QVector2D(e->localPos()) - this->mousePressPosition;

    // Rotation axis is perpendicular to the mouse position difference
    // vector
    QVector3D n = QVector3D(diff.y(), diff.x(), 0.0).normalized();

    // Accelerate angular speed relative to the length of the mouse sweep
    qreal acc = diff.length() / 90.0;

    // Calculate new rotation axis as weighted sum
    this->rotationAxis = (n * acc).normalized();

    // Increase angular speed
    this->angularSpeed = acc;
}

void OGLWidget::mouseReleaseEvent(QMouseEvent *e)
{
}

void OGLWidget::timerEvent(QTimerEvent *e)
{
    Q_UNUSED(e);

    // Decrease angular speed (friction)
    this->angularSpeed *= 0.99;

    // Stop rotation when speed goes below threshold
    if (this->angularSpeed < 0.01)
        this->angularSpeed = 0.0;
    else {
        // Update rotation
        this->rotation = QQuaternion::fromAxisAndAngle(
            this->rotationAxis,
            this->angularSpeed
        ) * this->rotation;

        // Update scene
        updateGL();
    }
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
