#ifndef OGLTEXTURE_H

#define OGLTEXTURE_H

#define GL3_PROTOTYPES 1

#include <string>
#include <iostream>
#include <GL3/gl3.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>

namespace OGLTexture {
	class OGLTexture {
	public:
		OGLTexture(void);
		OGLTexture(std::string filename);
		OGLTexture(OGLTexture const &src);
		~OGLTexture(void);

		bool Load(void);

		SDL_Surface* invertPixels(SDL_Surface *src) const;

		GLuint GetID(void) const;
		void SetFile(const std::string &filename);

		OGLTexture& operator=(OGLTexture const &src);

	private:
		// L'ID de la Texture
		GLuint id;
		std::string File;
	};
} /* OGLTexture */

#endif /* end of include guard: OGLTEXTURE_H */
