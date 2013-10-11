#include <stdio.h>
#include <stdlib.h>
#include "OGLTexture.hpp"

int load_image(const char *file)
{
	SDL_Surface *tex = IMG_Load(file); //SDL_LoadBMP(file);
	GLuint texture;

	printf("Status:  Loading image ");
	printf("%s", file);
	printf("... ");

	if(tex)
	{
		glGenTextures(1, &texture);
		glBindTexture(GL_TEXTURE_2D, texture);

		glTexImage2D(GL_TEXTURE_2D, 0, 3, tex->w, tex->h,
				0, GL_BGR, GL_UNSIGNED_BYTE, tex->pixels);

		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

		printf("OK\n");
		SDL_FreeSurface(tex);
	}
	else
	{
		printf("Failed\nQuitting...");
		SDL_Quit();
		exit(-1);
	}

	return texture;
}

namespace OGLTexture {
	OGLTexture::OGLTexture(void): id(0), File("")
	{
	}

	OGLTexture::OGLTexture(std::string filename): id(0), File(filename)
	{
	}

	OGLTexture::OGLTexture(OGLTexture const &src)
	{
		File = src.File;
		Load();
	}

	OGLTexture::~OGLTexture(void)
	{
		glDeleteTextures(1, &id);
	}

	OGLTexture& OGLTexture::operator=(OGLTexture const &src)
	{
		glDeleteTextures(1, &id);

		File = src.File;
		Load();

		return *this;
	}

	bool OGLTexture::Load(void)
	{
		// Chargement de la texture :
		SDL_Surface *tex = 0x0, *tmp = 0x0;
		if( (tmp = IMG_Load(File.c_str())) == 0x0 )
		{
			std::cerr << "Erreur : " << SDL_GetError() << std::endl;
			return false;
		}
		tex = invertPixels(tmp);
		SDL_FreeSurface(tmp);

		if( glIsTexture(id) == GL_TRUE )
			glDeleteTextures(1, &id);

		// Génération de l'ID :
		glGenTextures(1, &id);

		// Verrouillage de la texture pour permettre à OpenGL de
		// travailler dessus :
		glBindTexture(GL_TEXTURE_2D, id);

		if( tex->format->BytesPerPixel != 3 && tex->format->BytesPerPixel != 4 )
		{
			std::cerr << "Erreur : BytesPerPixel de la texture (" << (unsigned int)tex->format->BytesPerPixel << ") invalide (attendu : 3 ou 4)." << std::endl;
			SDL_FreeSurface(tex);
			return false;
		}

		GLenum format = (tex->format->BytesPerPixel == 3)?GL_RGB:GL_RGBA;

		glTexImage2D(GL_TEXTURE_2D, 0, tex->format->BytesPerPixel, tex->w, tex->h, 0, format, GL_UNSIGNED_BYTE, tex->pixels);

		// Doit améliorer la qualité du filtrage :
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

		// Applique un filtre au texture proche pour les lisser
		// (regarder les autres paramètres possibles en plus de
		// GL_LINEAR) :
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR); // */GL_LINEAR);

		// Applique un filtre pour pixeliser les textures les plus lointaines :
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

		// Génération du MipMap :
		glGenerateMipmap(GL_TEXTURE_2D);

		// Dévérrouillage de la texture :
		glBindTexture(GL_TEXTURE_2D, 0);

		SDL_FreeSurface(tex);
		return true;
	}

	SDL_Surface* OGLTexture::invertPixels(SDL_Surface *src) const
	{
		SDL_Surface   *copy = SDL_CreateRGBSurface(0, src->w, src->h, src->format->BitsPerPixel, src->format->Rmask, src->format->Gmask, src->format->Bmask, src->format->Amask);
		unsigned char *PSrc = (unsigned char*)src->pixels;
		unsigned char *PInv = (unsigned char*)copy->pixels;

		for(int i = 0; i < src->h; i++)
		{
			for(int j = 0; j < src->w * src->format->BytesPerPixel; j++)
			{
				PInv[src->w * src->format->BytesPerPixel*(src->h -1 - i) + j] = PSrc[i*src->w * src->format->BytesPerPixel + j];
			}
		}

		return copy;
	}

	GLuint OGLTexture::GetID(void) const
	{
		return id;
	}

	void OGLTexture::SetFile(const std::string &filename)
	{
		File = filename;
	}

} /* OGLTexture */
