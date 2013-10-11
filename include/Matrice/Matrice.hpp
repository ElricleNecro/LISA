#ifndef __MATRICE_H__
#define __MATRICE_H__

#include <iostream>
#include <iomanip>
#include "Matrice/reel.hpp"

#ifdef USE_LAPACK
extern "C"{
	//Les fonctions fortran utilisé :
	//	|-> Factorisation LU :
	void dgetrf_(int*,int*,float*,int*,int*,int*);
	//	|-> Inversion de matrice :
	void dgetri_(int*,float*,int*,int*,float*,int*,int*);
	//	|-> Resolution de systéme :
	void dgetrs_(char*,int*,int*,float*,int*,int*,float*,int*,int*);
	//		* 'N' => A*X=B
	//		* 'T' => A'*X=B (transposé)
	//		* 'C' => A'*X=B (conjugate transpose = transpose)
	//	|-> Valeurs propre :
	void dgeev_(char*,char*,int*,float*,int*,float*,float*,float*,int*,float*,int*,float*,int*,int*);
	//		1-'N' : Left Eigenvector of A are not computed
	//		  'V' :   "       "      "  "  "  computed
	//		2- Idem pour Right
};
#endif

class Matrice: public reel
{
	public:
		Matrice(int);
		Matrice(int, int);
		Matrice(const Matrice&);
		Matrice(const char*);

		virtual ~Matrice(void){};

		friend std::ostream& operator<<(std::ostream&, const Matrice&);
		Matrice& operator=(const Matrice&);
		Matrice  operator+(const Matrice&);
		Matrice  operator+(float);
		Matrice  operator-(const Matrice&);
		Matrice  operator-(float);
		Matrice  operator/(float);
		Matrice  operator*(const Matrice&);
		reel     operator*(const reel&);
		Matrice  operator*(float);

		using reel::operator();

#ifdef USE_LAPACK
		Matrice operator/(const Matrice&);
		Matrice inv(void);
		reel resout(const reel&);
		float det(void);
#endif
};

std::ostream& operator<<(std::ostream&, const Matrice&);
Matrice MatIdentity(const int dim);

#endif
