#ifndef INTERFACE_H

#define INTERFACE_H

#define GL3_PROTOTYPES 1
#include <GL3/gl3.h>

#include <string>
#include <QGLShader>

class Data {
	public:
		Data(const std::string& fname){};
		Data(const Data& old){};
		virtual ~Data(void){};

		virtual void Show(QGLShaderProgram &m_program, QMatrix4x4 &model){};
};

#endif /* end of include guard: INTERFACE_H */
