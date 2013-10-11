#ifndef OGLMATRICE_H

#define OGLMATRICE_H

#include <string>

#include "Matrice/Matrice.hpp"

namespace OGLMatrice {
	/* Classe de gestion des matrices OpenGL.
	 * Cette classe se base sur la classe d'opération matricielle créé à l'occasion du
	 * cours de C++ lors de mon année de M2 à l'Observatoire de Paris-Meudon. Cette classe
	 * arrive avec les opérations matricielles de base +,-,*.
	 * Si l'on active la compilation avec LAPACK, les opération de division, et résolution
	 * des systèmes linéaires seront disponible.
	 */
	class OGLMatrice: public Matrice {
		public:
			// Constructeurs et destructeur :
			OGLMatrice(void);
			OGLMatrice(float *val);
			OGLMatrice(Matrice const &arg);
			OGLMatrice(OGLMatrice const &arg);
			~OGLMatrice(void);

			// Quelques accesseurs :
			float const* GetValues(void) const;

			// Chargement de Matrice de Base.
			void LoadIdentity(void);
			void LoadPerspective(const float angle, const float ratio, const float near, const float far);

			// Transformation :
			void Translate(const float x, const float y, const float z);
			void Scale(const float x, const float y, const float z);
			void Rotate(float angle, const float x, const float y, const float z);
			void Projection(const float angle, const float ratio, const float near, const float far);

			// Autre type de transformation :
			void LookAt(const float eyeX, const float eyeY, const float eyeZ, const float centerX, const float centerY, const float centerZ, const float upX, const float upY, const float upZ);

			// Gestion de la Pile de matrice :
			bool push(void);
			bool pop(void);
			void Depiler(void);

			// Opérateur :
			using Matrice::operator=;
			using Matrice::operator+;
			using Matrice::operator-;
			using Matrice::operator*;
			using reel::operator();

		private:
			OGLMatrice *SavePrev;
	};

	/************************************************************************************************\
	 *			     Création de Matrice de base utile.					*
	\************************************************************************************************/
	/* Création de la Matrice Identité
	 * @return la matrice identité.
	 */
	OGLMatrice Identity(void);
	/* Création de la Matrice OpenGL de Perspective (ou de Projection).
	 * @param[in] angle Angle de vue ou FoV.
	 * @param[in] ratio Division de la Longueur de la fenêtre par sa Largeur : L/H (doit donnée des valeurs comme 4/3, 16/9, ...).
	 * @param[in] near  Distance entre l'écran et ce qui sera affiché. Zone non-affichable de l'écran.
	 * @param[in] far   Distance de vue maximale. Tout ce qui est au-delà ne sera pas affiché.
	 * @return La matrice de projection.
	 */
	OGLMatrice Perspective(const float angle, const float ratio, const float near, const float far);

	/* Création de la matrice de Translation.
	 * @param[in] x Translation sur l'axe x.
	 * @param[in] y Translation sur l'axe y.
	 * @param[in] z Translation sur l'axe z.
	 * @return La matrice de translation associé aux paramétre.
	 */
	OGLMatrice Translation(const float x, const float y, const float z);

	/* Création de la matrice de mise à l'echelle.
	 * @param[in] x Mise à l'echelle sur l'axe x.
	 * @param[in] y Mise à l'echelle sur l'axe y.
	 * @param[in] z Mise à l'echelle sur l'axe z.
	 * @return La matrice de mise à l'echelle associé aux paramétre.
	 */
	OGLMatrice Scaling(const float x, const float y, const float z);

	/* Création de la matrice de Rotation.
	 * @param[in] angle Angle de Rotation.
	 * @param[in] x     Rotation sur l'axe x.
	 * @param[in] y     Rotation sur l'axe y.
	 * @param[in] z     Rotation sur l'axe z.
	 * @return La matrice de Rotation associé aux paramétre.
	 */
	OGLMatrice Rotation(float angle, const float x, const float y, const float z);

	/* Création de la "matrice" caméra. La matrice sert à placer la caméra
	 * dans le monde et à l'orienter.
	 *
	 * Cette matrice à besoin de 9 paramètres qui peuvent être représenté
	 * comme étant les coordonnées de 3 vecteurs :
	 *	- vecteur Eye : place la caméra,
	 *	- vecteur Center : point vers lequel pointe la caméra,
	 *	- vecteur Up : normal (vertical) du repère.
	 * @param[in] eyeX Coordonnée X du vecteur Eye.
	 * @param[in] eyeY Coordonnée Y du vecteur Eye.
	 * @param[in] eyeZ Coordonnée Z du vecteur Eye.
	 * @param[in] centerX Coordonnée X du vecteur Center.
	 * @param[in] centerY Coordonnée Y du vecteur Center.
	 * @param[in] centerZ Coordonnée Z du vecteur Center.
	 * @param[in] upX Coordonnée X du vecteur Up.
	 * @param[in] upY Coordonnée Y du vecteur Up.
	 * @param[in] upZ Coordonnée Z du vecteur Up.
	 * @return La matrice de la camèra.
	 */
	OGLMatrice LookAtMatrice(const float eyeX, const float eyeY, const float eyeZ, const float centerX, const float centerY, const float centerZ, const float upX, const float upY, const float upZ);

	/* Retourne la norme d'un vecteur de N éléments.
	 * @param[in] *vect Vecteur dont on veut la norme.
	 * @param[in]  N    Taille du vecteur (N=3 si absent).
	 * @return Norme du vecteur.
	 */
	float Norme(const float *vect, const int N=3);

	/* Normalise un vecteur de N éléments.
	 * @param[inout] *vect Vecteur à normaliser.
	 * @param[in]     N    Taille du vecteur (N=3 si absent).
	 */
	void Normalise_Vect(float *vect, const int N=3);

	/*
	 */
	void PdtVect(float *res, const float *a, const float *b);
} /* OGLMatrice */

#endif /* end of include guard: OGLMATRICE_H */
