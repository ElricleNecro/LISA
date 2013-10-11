#include "Vecteur.hpp"

Vecteur::Vecteur(): x(0.0), y(0.0), z(0.0)
{
}

Vecteur::Vecteur(float xp, float yp, float zp): x(xp), y(yp), z(zp)
{
}

Vecteur::Vecteur(Vecteur const &v): x(v.x), y(v.y), z(v.z)
{
}

Vecteur::~Vecteur()
{
}

float Vecteur::GetX() const
{
	return x;
}

float Vecteur::GetY() const
{
	return y;
}

float Vecteur::GetZ() const
{
	return z;
}

void Vecteur::SetX(float xp)
{
	x = xp;
}

void Vecteur::SetY(float xp)
{
	y = xp;
}

void Vecteur::SetZ(float xp)
{
	z = xp;
}

void Vecteur::SetVecteur(float xp, float yp, float zp)
{
	x = xp;
	y = yp;
	z = zp;
}

void Vecteur::Normalise()
{
	float norm = std::sqrt(x*x + y*y + z*z);
	norm = (norm != 0.0)?norm:1.0;
	x /= norm;
	y /= norm;
	z /= norm;
}

Vecteur& Vecteur::operator=(const Vecteur &vecteur)
{
	// Copie des valeurs
	x = vecteur.x;
	y = vecteur.y;
	z = vecteur.z;

	// Retour de l'objet
	return *this;
}

Vecteur Vecteur::operator+(const Vecteur &vecteur)
{
	//Création d'un objet résultat
	Vecteur resultat;

	//Addition des coordonnées
	resultat.x=x+vecteur.x;
	resultat.y=y+vecteur.y;
	resultat.z=z+vecteur.z;

	return resultat;
}

Vecteur Vecteur::operator-(const Vecteur &vecteur)
{
	//Création d'un objet résultat
	Vecteur resultat;

	//Addition des coordonnées
	resultat.x=x-vecteur.x;
	resultat.y=y-vecteur.y;
	resultat.z=z-vecteur.z;

	return resultat;
}

Vecteur Vecteur::operator*(float multiplicateur)
{
	//Création d'un objet résultat
	Vecteur resultat;

	//Multiplication des coordonnées
	resultat.x=x*multiplicateur;
	resultat.y=y*multiplicateur;
	resultat.z=z*multiplicateur;


	//Retour du résultat
	return resultat;
}

Vecteur Vecteur::operator*(const Vecteur &vecteur)
{
	// Création d'un objet résultat
	Vecteur resultat;

	// Produit Vectoriel
	resultat.x = (y * vecteur.z) - (z * vecteur.y);
	resultat.y = (z * vecteur.x) - (x * vecteur.z);
	resultat.z = (x * vecteur.y) - (y * vecteur.x);

	// Retour de l'objet
	return resultat;
}

std::ostream& operator<<(std::ostream &o, const Vecteur &v)
{
	o << "(" << v.x << ", " << v.y << ", " << v.z << ")" << std::endl;
	return o;
}
