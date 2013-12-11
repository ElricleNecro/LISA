#include "oglwidget.hpp"

OGLWidget::OGLWidget(QWidget *parent) : QGLWidget(parent), program(new QGLShaderProgram(this)), cube()
{

    // Init the projection matrix to the identity
    this->projection.setToIdentity();

    // the same for the model matrix
    this->model.setToIdentity();

    // the same for the view matrix
    this->view.setToIdentity();

    // the initial distance
    this->distance = 2.5;

    // the angular speed for the rotation of the view
    this->angularSpeed = 0.0;

    // A timer to introduce a friction for the rotation by quaternions
    this->timer = new QBasicTimer();
}

// This function is called to initialize the OpenGL context which is
// created before this.
void OGLWidget::initializeGL()
{

    // enable evaluation of zorder
    glEnable(GL_DEPTH_TEST);

    // can't remember what is this
    glEnable(GL_CULL_FACE);

    // Put a black background for starting
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

// Called on resize of the widget by the user
void OGLWidget::resizeGL( int width, int height )
{

    // Check that the height is non null
    height = height?height:1;

    // Reset the projection matrix to the identity
    this->projection.setToIdentity();

    // Recompute the matrix for projection given the new size of the window
    this->projection.perspective(60.0, (float)width/(float)height, 0.001, 1000);

    // define the new length for the screen
    glViewport( 0, 0, width, height );
}

// Called to render the scene
void OGLWidget::paintGL(void)
{

    // Clear all on the buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    // Define the position of the camera initially
    QVector3D cameraPosition = QVector3D(0, 0, this->distance);

    // Define the up direction of the camera
    QVector3D cameraUpDirection = QVector3D(0, 1, 0);

    // Compute the view matrix to the position of the camera
    this->view.setToIdentity();
    this->view.lookAt(cameraPosition, QVector3D(0, 0, 0), cameraUpDirection);

    // Now rotate the view matrix with the movement of the camera applied
    // with the rotation obtained with the help of the "rotation" quaternion
    this->view.rotate(this->rotation);

    // bind the shaders
    program.bind();

    // Compute the global model-view-projection matrix
    QMatrix4x4 mMatrix;
    mMatrix = this->projection * this->view * this->model;

    // Display the cube with the shader program and the mvp matrix
    this->cube.Show(this->program, mMatrix);

    // release the shader program
    program.release();
}

// To init the size of the window ????
QSize OGLWidget::sizeHint() const
{
    return QSize(640, 480);
}

// kill the window when pressing escape
void OGLWidget::keyPressEvent( QKeyEvent *e )
{
    switch( e->key() )
    {
        case Qt::Key_Escape:
            close();
    }
}

// Store the position of the mouse on screen when pressing mouse
void OGLWidget::mousePressEvent(QMouseEvent *event)
{
    // Saving mouse press position
    this->mousePressPosition = QVector2D(event->localPos());
}

// When dragging the mouse, update the quaternion for the computation
// of the rotation induced by user movement
void OGLWidget::mouseMoveEvent(QMouseEvent *e)
{
    // Mouse release position - mouse press position
    QVector2D diff = QVector2D(e->localPos()) - this->mousePressPosition;

    // Rotation axis is perpendicular to the mouse position difference
    // vector
    QVector3D n = QVector3D(diff.y(), diff.x(), 0.0).normalized();

    // Accelerate angular speed relative to the length of the mouse sweep
    qreal acc = diff.length() / 90.0;

    // Calculate new rotation axis
    this->rotationAxis = (n * acc).normalized();

    // update angular speed
    this->angularSpeed = acc;
}

// If we want something when releasing the mouse
void OGLWidget::mouseReleaseEvent(QMouseEvent *e)
{
}

// A timer event manager to put a friction on the rotation induced by the
// user on the view matrix.
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

// To zoom in/out when rolling the wheel
void OGLWidget::wheelEvent(QWheelEvent *event)
{
    // The deplacement imposed by wheel
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
