#ifndef DEF_SHADER
#define DEF_SHADER

// Includes
#ifdef WIN32
	#include <GL/glew.h>
#elif __APPLE__
	#include <OpenGL/gl3.h>
#else
	#define GL3_PROTOTYPES 1
	#include <GL3/gl3.h>
#endif

#include <iostream>
#include <string>
#include <fstream>


namespace OpenGLShader {
	// Classe
	class Shader
	{
		// Méthodes publiques
		public:
			Shader(std::string vertexSource, std::string fragmentSource);
			Shader(Shader const &shader);
			~Shader();

			bool initialiser();
			void detruire();
			GLuint getProgramID() const;
			Shader& operator=(Shader const &shader);

		// Méthodes privées
		private:
			bool initialiserTypeShader(GLuint &shader, GLenum type, std::string const &source);
			void bindAttribLocation();

		// Attributs
		private:
			std::string m_vertexSource;
			std::string m_fragmentSource;

			GLuint m_vertexID;
			GLuint m_fragmentID;
			GLuint m_programID;

			bool m_initialise;
	};
}

#endif
