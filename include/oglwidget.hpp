#ifndef OGLWIDGET_HPP
#define OGLWIDGET_HPP

#include <GL3/gl3.h>
#include <GL/glu.h>

#include <QtOpenGL/QtOpenGL>
#include <QTimer>
#include <QQuaternion>
#include <QMouseEvent>

#include <iostream>

#include <stdexcept>

//#include "OGLCube.hpp"
#include "interface.hpp"

class OGLWidget : public QGLWidget
{
	Q_OBJECT
	public:
		OGLWidget(Data* fname, QWidget *parent = 0);
		QSize sizeHint() const;

	protected:
		virtual void initializeGL();
		virtual void resizeGL( int width, int height );
		virtual void paintGL();

		virtual void keyPressEvent( QKeyEvent *e );
		virtual void wheelEvent(QWheelEvent *event);
		virtual void mousePressEvent(QMouseEvent *event);
		virtual void mouseReleaseEvent(QMouseEvent *e);
		virtual void mouseMoveEvent(QMouseEvent *e);
		virtual void timerEvent(QTimerEvent *e);

	private:
		QGLShaderProgram program;
		QBasicTimer *timer;
		//OGLCube::OGLCube cube;
		Data *cube;
		QMatrix4x4 camera;
		QMatrix4x4 projection, model, view;
		QPoint lastMousePosition;
		QQuaternion rotation;
		QVector2D mousePressPosition;
		QVector3D rotationAxis;
		qreal angularSpeed;
		double distance;
};

#endif // OGLWIDGET_HPP
