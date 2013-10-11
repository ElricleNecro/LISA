#ifndef OGLCAMERA_HPP

#define OGLCAMERA_HPP

#include <cmath>
#include "Vecteur.hpp"
#include "OGLMatrice.hpp"

namespace OGLCamera {
	class OGLCamera {
		public:
			OGLCamera();
			OGLCamera(float posX, float posY, float posZ, float cibX, float cibY, float cibZ, float vertX, float vertY, float vertZ, float sens, float vit);
			~OGLCamera();

			void Oriente(int xRel, int yRel);
			void LookAt(OGLMatrice::OGLMatrice &modelview);

			void SetCible(float x, float y, float z);
			void SetPosition(float x, float y, float z);

			float GetSensibility(void) const;
			float GetVelocity(void) const;

			void SetSensibility(float val);
			void SetVelocity(float val);

		private:
			float phi, theta, sensibilite, vitesse;
			Vecteur dir, vert, lat, pos, cible;
	};
} /* OGLCamera */

#endif /* end of include guard: OGLCAMERA_HPP */
