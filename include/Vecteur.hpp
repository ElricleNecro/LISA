#ifndef VECTEUR_HPP

#define VECTEUR_HPP

#include <cmath>
#include <iostream>

//#define float double

class Vecteur {
	public:
		Vecteur();
		Vecteur(float x, float y, float z);
		Vecteur(Vecteur const &v);
		~Vecteur();

		/*setter et getter :*/
		float GetX() const;
		float GetY() const;
		float GetZ() const;

		void SetX(float x);
		void SetY(float x);
		void SetZ(float x);

		void SetVecteur(float x, float y, float z);

		void Normalise();

		friend std::ostream& operator<<(std::ostream&, const Vecteur&);

		Vecteur& operator=(const Vecteur &vecteur);
		Vecteur operator-(const Vecteur &vecteur);
		Vecteur operator+(const Vecteur &vecteur);
		Vecteur operator*(const Vecteur &vecteur);
		Vecteur operator*(float multiplicateur);

	private:
		float x, y, z;
};

std::ostream& operator<<(std::ostream&, const Vecteur&);

#endif /* end of include guard: VECTEUR_HPP */
