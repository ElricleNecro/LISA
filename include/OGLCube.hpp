#ifndef OGLCUBE_H

#define OGLCUBE_H

#define GL3_PROTOTYPES 1
#include <GL3/gl3.h>

#include <stdexcept>

#include <QGLShader>

namespace OGLCube {
	class OGLCube {
		public:
			OGLCube(void);
			OGLCube(float taille, std::string VerticeShader, std::string FragShader);
            virtual ~OGLCube(void);

            void Show(QGLShaderProgram &m_program, QMatrix4x4 &model);

        private:
			void init(void);

		protected:
			// Vertices et indices
            QVector<QVector3D> vertices;
            QVector<QVector3D> colors;
	};
};
#endif /* end of include guard: OGLCUBE_H */
