#include "Matrice/Matrice.hpp"

Matrice::Matrice(int a):reel(a, a)
{
}

Matrice::Matrice(int a, int b):reel(a, b)
{
}

Matrice::Matrice(const Matrice &arg):reel(arg)
{
}

Matrice::Matrice(const char *fich):reel(fich)
{
}

Matrice& Matrice::operator=(const Matrice &arg)
{
	reel::operator=(arg);
	return *this;
/*
	t1 = arg.t1;
	t2 = arg.t2;
	t3 = arg.t3;
	tot = arg.tot;
	tab = new float[tot];
	for(int i=0; i<tot; i++) tab[i] = arg.tab[i];
*/
}

Matrice Matrice::operator+(const Matrice &arg)
{
	if( t1 != arg.t1 || t2 != arg.t2 )
		throw std::string("Opération impossible, taille différente");
		//std::cerr<<"Op?ration impossible, taille diff?rente"<<std::endl,exit(EXIT_FAILURE);
	Matrice res(t1, t2);
	for(int i=0; i<tot; i++)
		res.tab[i] = tab[i] + arg.tab[i];
	return res;
}

Matrice Matrice::operator+(float arg)
{
	Matrice res(t1, t2);
	for(int i=0; i<tot; i++)
		res.tab[i] = tab[i] + arg;
	return res;
}

Matrice Matrice::operator-(const Matrice &arg)
{
	if( t1 != arg.t1 || t2 != arg.t2 )
		throw std::string("Opération impossible, taille différente");
		//std::cerr<<"Op?ration impossible, taille diff?rente"<<std::endl,exit(EXIT_FAILURE);
	Matrice res(t1, t2);
	for(int i=0; i<tot; i++)
		res.tab[i] = tab[i] - arg.tab[i];
	return res;
}

Matrice Matrice::operator-(float arg)
{
	Matrice res(t1, t2);
	for(int i=0; i<tot; i++)
		res.tab[i] = tab[i] - arg;
	return res;
}

Matrice Matrice::operator/(float arg)
{
	Matrice res(t1, t2);

	for(int i=0; i<tot; i++)
		res.tab[i] = tab[i]/arg;
	return res;
}

Matrice Matrice::operator*(const Matrice &arg)
{
	if( t2 != arg.t1 )
		throw std::string("Les Matrices ne peuvent pas etre multiplier ensemble");
		//std::cerr<<"Les Matrices ne peuvent pas etre multiplier ensemble"<<std::endl,exit(EXIT_FAILURE);
	Matrice res(t1, t2);

	/*
	11 12 13	11' 12' 13'		11*11'+12*21'+13*31' 11*
	21 22 23	21' 22' 23'	=
	31 32 33	31' 32' 33'
	*/
	for(int i=0; i<t1; i++)
		for(int j=0; j<arg.t2; j++)
		{
			res.tab[i+arg.t2*j]=0;
			for(int k=0; k<arg.t2; k++) //col1==lig2
			{
				res.tab[i+t2*j]+=arg.tab[i+arg.t2*k]*tab[k+arg.t2*j];
			}
		}

	return res;
}

reel Matrice::operator*(const reel &arg)
{
	//On verifie les dimension :
	if(arg.get_dim3() != 1)
		throw std::string("Les Matrices sont du type nxn, opération impossible");
		//std::cerr<<"Les Matrices sont du type nxn, op?ration impossible"<<std::endl,exit(EXIT_FAILURE);

	if(arg.get_dim2() != 1 && t2 != arg.get_dim1())
		throw std::string("Les Matrices ne peuvent pas etre multiplier ensemble");
		//std::cerr<<"Les Matrices ne peuvent pas etre multiplier ensemble"<<std::endl,exit(EXIT_FAILURE);

	if( arg.get_dim1() != t2)
		throw std::string("Les Matrices ne peuvent pas etre multiplier ensemble");
		//std::cerr<<"Les Matrices ne peuvent pas etre multiplier ensemble"<<std::endl,exit(EXIT_FAILURE);

	reel res(arg.get_dim1());
	for(int i=0; i<t1; i++)
	{
		res(i)=0;
		for(int k=0; k<t2; k++) //col1==lig2
		{
			res(i)+=tab[i+arg.get_dim2()*k]*arg(k);
		}
	}
	return res;
}

#ifdef USE_LAPACK
Matrice Matrice::operator/(const Matrice &arg)
{
	//On inverse arg, puis on multiplie
	//Matrice tmp = arg.inv();
	if( t1 != t2 )
		throw std::string("Impossible : Matrice non-carrée!!!");
		//std::cerr<<"Impossible : Matrice non-carr?e!!!"<<std::endl,exit(EXIT_FAILURE);
	//On recopie les tableux source :
	float *tmpt   = new float[tot];
	int    *pivot  = new int[tot];
	float *B      = new float[t1];

	for(int i=0; i<tot; i++)
	{
		tmpt[i] = tab[i];
	}
	for(int i=0; i<t1; i++)
	{
		B[i]   = 0;
	}

	//On factorise la Matrice :
	int info;
	int t1_ = t1;
	dgetrf_(&t1_, &t1_, tmpt, &t1_, pivot, &info);

	if(info < 0)
	{
		std::cerr<<"\033[31mArgument "<<-info<<" Valeur ill?gal\033[00m"<<std::endl;
		throw -info;
		//std::cerr<<"\033[31mArgument "<<-info<<" Valeur ill?gal\033[00m"<<std::endl,exit(EXIT_FAILURE);
	}
	if(info > 0)
	{
		std::cerr<<"\033[31mU("<<info<<", "<<info<<") est exactement 0, risque de division par 0\033[00m"<<std::endl;
		throw info;
	}

	int t2_ = t1;
	dgetri_(&t1_, tmpt, &t1_, pivot, B, &t2_, &info);

	if(info < 0)
	{
		std::cerr<<"\033[31mArgument "<<-info<<" : Valeur ill?gal\033[00m"<<std::endl;
		throw info;
		//std::cerr<<"\033[31mArgument "<<-info<<" : Valeur ill?gal\033[00m"<<std::endl,exit(EXIT_FAILURE);
	}
	if(info > 0)
	{
		std::cerr<<"\033[31mU("<<info<<", "<<info<<") est exactement 0, la Matrice est singuli?re et ne peut-etre calcul?e.\033[00m"<<std::endl;
		throw info;
	}

	Matrice tmp(t1, t2);
	for(int i=0; i<tot; i++)
		tmp.tab[i] = tmpt[i];

	if( t2 != tmp.t1 )
	{
		//std::cerr<<"Les Matrices ne peuvent pas etre multiplier ensemble"<<std::endl,exit(EXIT_FAILURE);
		throw std::string("Les Matrices ne peuvent pas etre multiplier ensemble");
	}
	Matrice res(t1, t2);

	/*
	11 12 13	11' 12' 13'		11*11'+12*21'+13*31' 11*
	21 22 23	21' 22' 23'	=
	31 32 33	31' 32' 33'
	*/
	for(int i=0; i<t1; i++)
		for(int j=0; j<tmp.t2; j++)
		{
			res.tab[i+tmp.t2*j]=0;
			for(int k=0; k<tmp.t2; k++) //col1==lig2
			{
				res.tab[i+t2*j]+=tab[i+tmp.t2*k]*tmp.tab[k+tmp.t2*j];
			}
		}

	return res;
}

float Matrice::det(void)
{
	if( t1 != t2 )
	{
		//std::cerr<<"Impossible de calculer un determinant : Matrice non-carr?e!!!"<<std::endl,exit(EXIT_FAILURE);
		throw std::string("Impossible de calculer un determinant : Matrice non-carrée!!!");
	}
	char JOBL = 'N', JOBR = 'N';
	int t1_   = t1,
	    LWORK = 3*t1,
		INFO;
	float *A    = new float[tot],
	       *WR   = new float[t1],
	       *WI   = new float[t1],
	       *VL   = new float[tot],
	       *VR   = new float[tot],
	       *WORK = new float[LWORK];

	for(int i=0; i<tot; i++)
		A[i] = tab[i];

	dgeev_(&JOBL, &JOBR, &t1_, A, &t1_, WR, WI, VL, &t1_, VR, &t1_, WORK, &LWORK, &INFO);

	/*
		(a+ib)*(c+id) = a*c - b*d + i(a*d + b*c)
	*/

	if(INFO < 0)
	{
		std::cerr<<"\033[31mArgument "<<-INFO<<" : Valeur illégal\033[00m"<<std::endl; //,exit(EXIT_FAILURE);
		throw INFO;
	}
	if(INFO > 0)
	{
		std::cerr<<"\033[31mL'algorithme QR a échoué à calculer les valeurs propres à partir de "<<INFO+1<<":N de WR. Les Valeurs imaginaires WI ont convergé.\033[00m"<<std::endl;
		throw INFO+1;
	}

	float rdet = 1, idet = 1, tmp = 1;
	for(int i=0; i<t1; i++)
	{
//		rdet *= WR[i]*rdet - WI[i]*idet;
//		idet *= WR[i]*idet + WI[i]*rdet;
		tmp *= WR[i];
//		std::cerr<<"\033[31m"<<rdet<<"\033[00m"<<std::endl;
//		std::cerr<<"\033[31m"<<idet<<"\033[00m"<<std::endl;
		std::cerr<<"\033[31m"<<tmp<<"\033[00m"<<std::endl;
	}

//	return rdet;
	return tmp;
}

Matrice Matrice::inv(void)
{
	if( t1 != t2 )
	{
		//std::cerr<<"Impossible : Matrice non-carr?e!!!"<<std::endl,exit(EXIT_FAILURE);
		throw std::string("Impossible : Matrice non-carrée!!!");
	}
	//On recopie les tableux source :
	float *tmp   = new float[tot];
	int    *pivot = new int[tot];
	float *B     = new float[t1];

	for(int i=0; i<tot; i++)
	{
		tmp[i] = tab[i];
	}
	for(int i=0; i<t1; i++)
	{
		B[i]   = 0;
	}

	//On factorise la Matrice :
	int info;
	int t1_ = t1;
	dgetrf_(&t1_, &t1_, tmp, &t1_, pivot, &info);

	if(info < 0)
	{
		std::cerr<<"\033[31mArgument "<<-info<<" Valeur illégal\033[00m"<<std::endl; //,exit(EXIT_FAILURE);
		throw info;
	}
	if(info > 0)
	{
		std::cerr<<"\033[31mU("<<info<<", "<<info<<") est exactement 0, risque de division par 0\033[00m"<<std::endl;
		throw info;
	}

	int t2_ = t1;
	dgetri_(&t1_, tmp, &t1_, pivot, B, &t2_, &info);

	if(info < 0)
	{
		std::cerr<<"\033[31mArgument "<<-info<<" : Valeur ill?gal\033[00m"<<std::endl; //,exit(EXIT_FAILURE);
		throw info;
	}
	if(info > 0)
	{
		std::cerr<<"\033[31mU("<<info<<", "<<info<<") est exactement 0, la Matrice est singuli?re et ne peut-etre calcul?e.\033[00m"<<std::endl;
		throw info;
	}

	Matrice res(t1, t2);
	for(int i=0; i<tot; i++)
		res.tab[i] = tmp[i];

	delete[] tmp;
	delete[] pivot;
	delete[] B;

	return res;
}

reel Matrice::resout(const reel &arg)
{
	if( t1 != t2 )
	{
		//std::cerr<<"Impossible : Matrice non-carr?e!!!"<<std::endl,exit(EXIT_FAILURE);
		throw std::string("Impossible : Matrice non-carrée!!!");
	}
	//On recopie les tableux source :
	float *tmp   = new float[tot];
	int    *pivot = new int[tot];
	float *B     = new float[arg.get_dim1()];
	reel   res(arg.get_dim1());
	for(int i=0; i<tot; i++)
	{
		tmp[i] = tab[i];
	}
	for(int i=0; i<arg.get_dim1(); i++)
	{
		B[i]   = arg(i);
	}

	//On factorise la Matrice :
	int info;
	int t1_ = t1;
	dgetrf_(&t1_, &t1_, tmp, &t1_, pivot, &info);

	if(info < 0)
	{
		std::cerr<<"\033[31mArgument "<<-info<<" : Valeur ill?gal\033[00m"<<std::endl; //,exit(EXIT_FAILURE);
		throw info;
	}
	if(info > 0)
	{
		std::cerr<<"\033[31mU("<<info<<", "<<info<<") est exactement 0, risque de division par 0\033[00m"<<std::endl;
		throw info;
	}

	int NRHS = 0,
	    t1__ = arg.get_dim1();
	char type='T'; //On prend la transpos? car le stockage des tableau en C et Fortran n'est pas le meme.

	//On resout le syst?me :
	dgetrs_(&type, &t1_, &NRHS, tmp, &t1_, pivot, B, &t1__, &info);

	for(int i=0; i<arg.get_dim1(); i++) res(i) = B[i];

	return res;
}
#endif

std::ostream& operator<<(std::ostream &o, const Matrice &arg)
{
	o << std::fixed << std::setprecision(4) << std::showpos;
	for(int a=0; a<arg.tot; a++)
	{
		o<<arg.tab[a]<<" ";
		if( (arg.t2 != 1 && ((a+1)%(arg.t2)==0)) || (arg.t3 != 1 && ((a+1)%(arg.t3)==0)) )
			o<<std::endl;
	}
	return o;
}

Matrice MatIdentity(const int dim)
{
	Matrice A(dim);
	for(int i = 0; i < dim; i++)
	{
		A(i, i) = 1.0;
	}
	return A;
}

