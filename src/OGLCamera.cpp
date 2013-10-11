#include "OGLCamera.hpp"

namespace OGLCamera {
	OGLCamera::OGLCamera(): phi(0.0), theta(0.0), sensibilite(0.0), vitesse(0.0), dir(), vert(0.0, 0.0, 1.0), lat(), pos(), cible()
	{
		SetCible(cible.GetX(), cible.GetY(), cible.GetZ());
	}

	OGLCamera::OGLCamera(float posX, float posY, float posZ, float cibX, float cibY, float cibZ, float vertX, float vertY, float vertZ, float sens, float vit): phi(0.0), theta(0.0), sensibilite(sens), vitesse(vit), dir(), vert(vertX, vertY, vertZ), lat(), pos(posX, posY, posZ), cible(cibX, cibY, cibZ)
	{
		SetCible(cibX, cibY, cibZ);
	}

	OGLCamera::~OGLCamera()
	{
	}

	void OGLCamera::SetCible(float x, float y, float z)
	{
		cible.SetX(x);
		cible.SetY(y);
		cible.SetZ(z);

		dir = cible - pos;
		dir.Normalise();

		if( vert.GetX() == 1.0 )
		{
			phi   = std::asin(dir.GetX());
			theta = std::acos(dir.GetY() / std::cos(phi));
			if( dir.GetZ() < 0 )
				theta *= -1.0;
		}
		else if( vert.GetY() == 1.0 )
		{
			phi   = std::asin(dir.GetY());
			theta = std::acos(dir.GetZ() / std::cos(phi));
			if( dir.GetZ() < 0 )
				theta *= -1.0;
		}
		else
		{
			phi   = std::asin(dir.GetX());
			theta = std::acos(dir.GetZ() / std::cos(phi));
			if( dir.GetZ() < 0 )
				theta *= -1.0;
		}

		phi = phi * 180.0 / M_PI;
		theta = theta * 180.0 / M_PI;
	}

	void OGLCamera::SetPosition(float x, float y, float z)
	{
		pos.SetX(x);
		pos.SetY(y);
		pos.SetZ(z);

		cible = pos + dir;
	}

	void OGLCamera::Oriente(int xRel, int yRel)
	{
		phi   += -sensibilite*yRel;
		theta += -sensibilite*xRel;

		if( phi > 89.0 )
			phi = 89.0;
		else if( phi < -89.0 )
			phi = -89.0;

		if( vert.GetX() == 1.0 )
		{
			dir.SetX(std::sin(phi * M_PI/180.0));
			dir.SetY(std::cos(phi * M_PI/180.0) * std::cos(theta * M_PI/180.0));
			dir.SetZ(std::cos(phi * M_PI/180.0) * std::sin(theta * M_PI/180.0));
		}
		else if( vert.GetY() == 1.0 )
		{
			dir.SetX(std::cos(phi * M_PI/180.0) * std::sin(theta * M_PI/180.0));
			dir.SetY(std::sin(phi * M_PI/180.0));
			dir.SetZ(std::cos(phi * M_PI/180.0) * std::cos(theta * M_PI/180.0));
		}
		else
		{
			dir.SetX(std::cos(phi * M_PI/180.0) * std::sin(theta * M_PI/180.0));
			dir.SetY(std::cos(phi * M_PI/180.0) * std::cos(theta * M_PI/180.0));
			dir.SetZ(std::sin(phi * M_PI/180.0));
		}

		lat = vert * dir;
		lat.Normalise();

		cible = dir + pos;
	}

    //void OGLCamera::Deplacer(SDLInput::SDLInput const &input)
    //{
        //if( input.MoveDone() )
            //Oriente(input.GetXRel(), input.GetYRel() );

        //if( input.GetKey(SDL_SCANCODE_UP) )
        //{
            //pos = pos + dir * vitesse;
            //cible = pos + dir;
        //}

        //if( input.GetKey(SDL_SCANCODE_DOWN) )
        //{
            //pos = pos - dir * vitesse;
            //cible = pos + dir;
        //}

        //if( input.GetKey(SDL_SCANCODE_LEFT) )
        //{
            //pos = pos + lat * vitesse;
            //cible = pos + dir;
        //}

        //if( input.GetKey(SDL_SCANCODE_RIGHT) )
        //{
            //pos = pos - lat * vitesse;
            //cible = pos + dir;
        //}
    //}

	void OGLCamera::LookAt(OGLMatrice::OGLMatrice &modelview)
	{
		modelview.LookAt(pos.GetX(), pos.GetY(), pos.GetZ(), cible.GetX(), cible.GetY(), cible.GetZ(), vert.GetX(), vert.GetY(), vert.GetZ());
	}

	float OGLCamera::GetSensibility(void) const
	{
		return sensibilite;
	}

	float OGLCamera::GetVelocity(void) const
	{
		return vitesse;
	}

	void OGLCamera::SetSensibility(float val)
	{
		sensibilite = val;
	}

	void OGLCamera::SetVelocity(float val)
	{
		vitesse = val;
	}
} /* OGLCamera */
