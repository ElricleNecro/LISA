#ifndef OGLCUBE_H

#define OGLCUBE_H

#define GL3_PROTOTYPES 1
#include <GL3/gl3.h>

#include <stdexcept>

#include <QGLShader>
//#include <QOpenGLShaderProgram>

#include "Shader.hpp"
#include "OGLMatrice.hpp"
#ifdef TEXTURE_ACTIVATE
#include "OGLTexture.hpp"
#endif

namespace OGLCube {
	class OGLCube {
		public:
			OGLCube(void);
			OGLCube(float taille, std::string VerticeShader, std::string FragShader);
            virtual ~OGLCube(void);

            void Show(QGLShaderProgram &m_program, OGLMatrice::OGLMatrice &proj, OGLMatrice::OGLMatrice &model);

        private:
			void init(void);

		protected:
                        //OpenGLShader::Shader shader;
                        //QOpenGLShaderProgram m_program;
			// Vertices et indices
			float       *vertices;
			unsigned int *indices;
			// Couleurs
			float       *rouge, *vert, *bleu;
			// Taille du cube
			float taille;
	};

#ifdef TEXTURE_ACTIVATE
    class OGLTexturedCube : public OGLCube {
		public:
			OGLTexturedCube(void);
			OGLTexturedCube(float taille, std::string VerticeShader, std::string FragShader, std::string text);
			//void Show(OGLMatrice::OGLMatrice &proj, OGLMatrice::OGLMatrice &model);

		private:
			OGLTexture::OGLTexture texture;
			float *texture_coord;
	};
#endif
} /* OGLCube */

#endif /* end of include guard: OGLCUBE_H */
