#ifndef __REEL_H__
#define __REEL_H__

#include<cstdlib>
#include<iostream>
#include<fstream>
#include<cmath>

class reel {
	protected:
		float *tab;
		int t1, t2, t3, tot;

	public:
		//Constructeur :
		reel(int a, int b=1, int c=1);
//		reel(float*, int);
		reel(const reel&);
		reel(const char*);

		//Destructeur :
		virtual ~reel(void);

		//Accesseur :
		inline int get_dim1(void) const {return t1;};
		inline int get_dim2(void) const {return t2;};
		inline int get_dim3(void) const {return t3;};
		float& set(int i, int j=0, int z=0);

		//operateur :
		friend std::ostream& operator<<(std::ostream&, const reel&);
		friend reel operator-(const reel &arg);
		friend reel operator*(const float,const reel&);
		reel& operator=(const reel&);
		reel& operator=(const float);
		float& operator()(int a, int b=0, int c=0);
		float operator()(int a, int b=0, int c=0) const ;
		reel operator+(const float);
		reel operator-(const float);
		reel operator-(const reel&);
		reel operator/(const reel&);
		reel operator*(const reel&);
		reel operator*(const float) const;

		//Fonction Autre :
		void save(const char*) const;
		void sauve(const char*) const;
		float max(void) const;

		friend class matrice;
};

std::ostream& operator<<(std::ostream&, const reel&);
reel operator-(const reel &arg);
reel operator*(const float,const reel&);

reel exp(const reel&);
reel sin(const reel&);
reel abs(const reel&);

float max(const reel&);

reel PdtVect3D(const reel& a, const reel& b);

#endif
