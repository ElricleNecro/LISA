#include "OGLMatrice.hpp"

namespace OGLMatrice {
	OGLMatrice::OGLMatrice(void):Matrice(4), SavePrev(0)
	{
		for(int i = 0; i < t1*t2; i++)
		{
			tab[i] = 0.0;
		}
	}

	OGLMatrice::OGLMatrice(OGLMatrice const &arg): Matrice(4), SavePrev(0)
	{
		t1 = arg.t1;
		t2 = arg.t2;
		t3 = 1;
		for(int i = 0; i < t1*t2; i++)
		{
			tab[i] = arg.tab[i];
		}
	}

	OGLMatrice::OGLMatrice(Matrice const &arg): Matrice(4), SavePrev(0)
	{
		if(arg.get_dim1() != 4 && arg.get_dim2() != 4 && arg.get_dim3() != 1)
			throw std::string("La Matrice n'a pas les bonnes dimensions");

		t1 = arg.get_dim1();
		t2 = arg.get_dim2();
		t3 = 1;
		for(int i = 0; i < t1*t2; i++)
		{
			tab[i] = arg(i);
		}
	}

	OGLMatrice::OGLMatrice(float *val):Matrice(4), SavePrev(0)
	{
		for(int i = 0; i < t1*t2; i++)
		{
			tab[i] = val[i];
		}
	}

	OGLMatrice::~OGLMatrice(void)
	{
		Depiler();
		if( tab != 0x0 )
		{
			delete[] tab;
			tab = 0x0;
		}
	}

	float const* OGLMatrice::GetValues(void) const
	{
		return (float const*)tab;
	}
//	OGLMatrice OGLMatrice::operator*(const OGLMatrice const &arg)
//	{
//		return OGLMatrice(Matrice::operator*(arg));
//	}
//
//	OGLMatrice OGLMatrice::operator+(const OGLMatrice const &arg)
//	{
//		return OGLMatrice(Matrice::operator+(arg));
//	}
//
//	OGLMatrice OGLMatrice::operator-(const OGLMatrice const &arg)
//	{
//		return OGLMatrice(Matrice::operator-(arg));
//	}
	void OGLMatrice::LoadIdentity(void)
	{
		Depiler();
		*this = Identity();
	}

	void OGLMatrice::LoadPerspective(const float angle, const float ratio, const float near, const float far)
	{
		Depiler();
		*this = Perspective(angle, ratio, near, far);
	}

	void OGLMatrice::Translate(const float x, const float y, const float z)
	{
		*this = *this * Translation(x, y, z);
	}

	void OGLMatrice::Scale(const float x, const float y, const float z)
	{
		*this = *this * Scaling(x, y, z);
	}

	void OGLMatrice::Rotate(float angle, const float x, const float y, const float z)
	{
		*this  = *this * Rotation(angle, x, y, z);
	}

	void OGLMatrice::Projection(const float angle, const float ratio, const float near, const float far)
	{
		*this = *this * Perspective(angle, ratio, near, far);
	}

	void OGLMatrice::LookAt(const float eyeX, const float eyeY, const float eyeZ, const float centerX, const float centerY, const float centerZ, const float upX, const float upY, const float upZ)
	{
//		std::cout<<eyeX<<" "<<eyeY<<" "<<eyeZ<<std::endl;
		*this = *this * LookAtMatrice(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ);
//		std::cout << *this << std::endl << std::endl;
		Translate(-eyeX, -eyeY, -eyeZ);
//		std::cout << *this << std::endl;
	}

	bool OGLMatrice::push(void)
	{
		OGLMatrice *newcase = new OGLMatrice;

		if( newcase == 0 )
			return false;

		*newcase = *this;
		newcase->SavePrev = SavePrev;
		SavePrev = newcase;

		return true;
	}

	bool OGLMatrice::pop(void)
	{
		OGLMatrice *tmp = SavePrev;

		if( tmp == 0 )
			return false;

		*this = *tmp;
		SavePrev  = tmp->SavePrev;

		tmp->SavePrev = 0;
		delete tmp;

		return true;
	}

	void OGLMatrice::Depiler(void)
	{
		while(pop());
	}

	OGLMatrice Identity(void)
	{
		OGLMatrice A;
		for(int i = 0; i < A.get_dim1(); i++)
		{
			A(i, i) = 1.0;
		}
		return A;
	}

	OGLMatrice Translation(const float x, const float y, const float z)
	{
		OGLMatrice A(Identity());
		A(0, A.get_dim1()-1) = x;
		A(1, A.get_dim1()-1) = y;
		A(2, A.get_dim1()-1) = z;

		return A;
	}

	OGLMatrice Scaling(const float x, const float y, const float z)
	{
		OGLMatrice A;
		A(0, 0) = x;
		A(1, 1) = y;
		A(2, 2) = z;
		A(3, 3) = 1.0;
		return A;
	}

	OGLMatrice Rotation(float angle, const float x, const float y, const float z)
	{
		OGLMatrice A;
		float axe[3] = {x, y, z};

		Normalise_Vect(axe);

		angle *= std::acos(-1.0)/180.0;

		A(0, 0) = axe[0]*axe[0] * (1 - std::cos(angle)) +        std::cos(angle);
		A(0, 1) = axe[0]*axe[1] * (1 - std::cos(angle)) - axe[2]*std::sin(angle);
		A(0, 2) = axe[0]*axe[2] * (1 - std::cos(angle)) + axe[1]*std::sin(angle);

		A(1, 0) = axe[0]*axe[1] * (1 - std::cos(angle)) + axe[2]*std::sin(angle);
		A(1, 1) = axe[1]*axe[1] * (1 - std::cos(angle)) +        std::cos(angle);
		A(1, 2) = axe[1]*axe[2] * (1 - std::cos(angle)) - axe[0]*std::sin(angle);

		A(2, 0) = axe[0]*axe[2] * (1 - std::cos(angle)) - axe[1]*std::sin(angle);
		A(2, 1) = axe[1]*axe[2] * (1 - std::cos(angle)) + axe[0]*std::sin(angle);
		A(2, 2) = axe[2]*axe[2] * (1 - std::cos(angle)) +        std::cos(angle);

		//A(3, 0) = 1.0;
		A(3, 3) = 1.0;

		//std::cout << A << std::endl << std::endl;

		return A;
	}

	float Norme(const float *vect, const int N)
	{
		float sum = 0.0;
		for(int i = 0; i < N; i++)
		{
			sum += vect[i]*vect[i];
		}
		return std::sqrt(sum);
	}

	void Normalise_Vect(float *vect, const int N)
	{
		float norm = Norme(vect, N);
		norm = (norm != 0.0)?norm:1.0;
		for(int i = 0; i < N; i++)
		{
			vect[i] /= norm;
		}
	}

	OGLMatrice Perspective(const float angle, const float ratio, const float near, const float far)
	{
		OGLMatrice projection;
		float     f = 1.0/std::tan( (angle/2.0) * M_PI / 180.0);

		projection(0, 0) = f / ratio;
		projection(1, 1) = f;
		projection(2, 2) = (near + far) / (near - far);
		projection(2, 3) = 2.0 * near * far / (near - far);
		projection(3, 2) = -1.0;

		return projection;
	}

	void PdtVect(float *res, const float *a, const float *b)
	{
		res[0] = a[1] * b[2] - a[2] * b[1];
		res[1] = a[2] * b[0] - a[0] * b[2];
		res[2] = a[0] * b[1] - a[1] * b[0];
	}

	OGLMatrice LookAtMatrice(const float eyeX, const float eyeY, const float eyeZ, const float centerX, const float centerY, const float centerZ, const float upX, const float upY, const float upZ)
	{
		float axe[3]    = {upX, upY, upZ};
		float regard[3] = {centerX - eyeX, centerY - eyeY, centerZ - eyeZ};
		float normal[3] = {0};
		float newAxe[3] = {0};

		OGLMatrice A;

		PdtVect(normal, regard, axe);
		PdtVect(newAxe, normal, regard);

//		for(int i = 0; i < 3; i++)
//		{
//			std::cout << std::showpos << std::fixed << std::setprecision(5) << normal[i] << "\t" << newAxe[i] << "\t" << regard[i] << std::endl;
//		}
//		std::cout << std::endl;

		Normalise_Vect(normal);
		Normalise_Vect(newAxe);
		Normalise_Vect(regard);

//		for(int i = 0; i < 3; i++)
//		{
//			std::cout << std::showpos << std::fixed << std::setprecision(5) << normal[i] << "\t" << newAxe[i] << "\t" << regard[i] << std::endl;
//		}
//		std::cout << std::endl;

		A(0, 0) = normal[0];
		A(0, 1) = normal[1];
		A(0, 2) = normal[2];

		A(1, 0) = newAxe[0];
		A(1, 1) = newAxe[1];
		A(1, 2) = newAxe[2];

		A(2, 0) = -regard[0];
		A(2, 1) = -regard[1];
		A(2, 2) = -regard[2];

		//A(3, 0) = -10.0;
		A(3, 3) = 1.0;

//		std::cout << A << std::endl << std::endl;

		return A;
	}
} /* OGLMatrice */
