#include "Matrice/reel.hpp"

reel::reel(int a, int b, int c):tab(0x0),t1(a),t2(b),t3(c),tot(a*b*c)
{
	tab = new float[tot];
	if(tab == 0x0)
		std::cerr<<"\033[31mErreur d'allocation\033[00m"<<std::endl,exit(EXIT_FAILURE);
}

reel::reel(const reel &arg):tab(0x0),t1(arg.t1),t2(arg.t2),t3(arg.t3),tot(arg.t1*arg.t2*arg.t3)
{
	tab = new float[tot];
	if(tab == 0x0)
		std::cerr<<"i\033[31mErreur d'allocation\033[00m"<<std::endl,exit(EXIT_FAILURE);
	for(int i=0; i<tot; i++)
		tab[i] = arg.tab[i];
}

reel::reel(const char *file_name):tab(0x0)
{
	std::ifstream fich(file_name);
	//Récupération des tailles :
	fich>>t1;
	fich>>t2;
	fich>>t3;
	tot = t1*t2*t3;
	//Récupération des données :
	tab = new float[tot];
	for(int i=0; i<tot; i++)
		fich>>tab[i];
	fich.close();
	if(tab == 0x0)
		std::cerr<<"\033[31mErreur d'allocation\033[00m"<<std::endl,exit(EXIT_FAILURE);
}

reel::~reel(void)
{
	if( tab != 0x0 )
	{
		delete[] tab;
		tab = 0x0;
	}
}

float& reel::set(int i, int j, int z)
{
	if(i > t1 || j > t2 || z > t3)
		std::cerr<<"\033[31mErreur, argument incompatible avec la taille des tableaux.\033[00m"<<std::endl,exit(EXIT_FAILURE);
	return tab[i + j*t1 + z*t2]; //tab[i*t1 + j*t2 + z];
}

reel& reel::operator=(const reel &arg)
{
	t1 = arg.t1;
	t2 = arg.t2;
	t3 = arg.t3;
	tot = arg.tot;

//	if(tab != 0x0)
	delete[] tab;
        tab = new float[tot];
        for(int i=0; i<tot; i++)
                tab[i] = arg.tab[i];
	return *this;
}

reel& reel::operator=(const float val)
{
	for(int i=0; i<tot; i++)
		tab[i] = val;
	return *this;
}

float& reel::operator()(int a, int b, int c)
{
	if(a > t1 || b > t2 || c > t3)
		std::cerr<<"\033[31mErreur, argument incompatible avec la taille des tableaux.\033[00m"<<std::endl,exit(EXIT_FAILURE);
	return tab[a*t1 + b + c*t2];
}

float reel::operator()(int a, int b, int c) const
{
	if(a > t1 || b > t2 || c > t3)
                std::cerr<<"\033[31mErreur, argument incompatible avec la taille des tableaux.\033[00m"<<std::endl,exit(EXIT_FAILURE);
        return tab[b + a*t1 + c*t2];
}

reel reel::operator+(const float val)
{
	reel tmp(t1, t2, t3);
	for(int i=0; i<tot; i++)
		tmp.tab[i]= tab[i] + val;
	return tmp;
}

reel reel::operator-(const float val)
{
	reel tmp(t1, t2, t3);
	for(int i=0; i<tot; i++)
		tmp.tab[i]= tab[i] - val;
	return tmp;
}

reel reel::operator-(const reel &arg)
{
	if(arg.t1 != t1 || arg.t2 != t2 || arg.t3 != t3)
		std::cerr<<"Erreur, les tableaux n'ont pas la meme dimension"<<std::endl,exit(EXIT_FAILURE);

	reel res(t1, t2, t3);
	for(int i=0; i<tot; i++)
		res(i) = tab[i] - arg(i);
	return res;
}

reel reel::operator/(const reel &arg)
{
	reel tmp(t1, t2, t3);
	for(int i=0; i<tot; i++)
                tmp.tab[i] = tab[i] / arg.tab[i];
	return tmp;
}

reel reel::operator*(const reel &arg)
{
	if(tot != arg.tot)
		std::cerr<<"\033[31mLes tableaux ne sont pas de la meme taille"<<std::endl,exit(EXIT_FAILURE);
	reel res(t1, t2, t3);
	for(int i=0; i<tot; i++)
		res(i) = tab[i]*arg.tab[i];
	return res;
}

reel reel::operator*(const float cte) const
{
	reel res(t1, t2, t3);
	for(int i=0; i<tot; i++) res(i) = tab[i]*cte;
	return res;
}

std::ostream& operator<<(std::ostream& o, const reel& arg)
{
/*	for(int i=0; i<arg.t1; i++)
	{
		int j;
		for(j=0; j<arg.t2; j++)
		{
			int z;
			for(z=0; z<arg.t3; z++)
				o<<arg.tab[i*arg.t1 + j*arg.t2 + z]<<" ";
			o<<std::endl;
		}
		o<<std::endl;
	}

	o<<std::endl;
*/	for(int a=0; a<arg.tot; a++)
	{
		o<<arg.tab[a]<<" ";
		if( (arg.t2 != 1 && ((a+1)%(arg.t2)==0)) || (arg.t3 != 1 && ((a+1)%(arg.t3)==0)))
			o<<std::endl;
	}
	return o;
}

void reel::save(const char *file) const
{
	sauve(file);
}

void reel::sauve(const char *file) const
{
	std::ofstream fich(file);
	fich<<t1<<std::endl;
	fich<<t2<<std::endl;
	fich<<t3<<std::endl;

	for(int i=0; i<tot; i++)
		fich<<tab[i]<<" ";

	fich.close();
}

float reel::max(void) const
{
	float m_max = tab[0];
	for(int i=0; i<tot; i++)
		if(tab[i]>tab[0])
			m_max = tab[i];
	return m_max;
}

reel exp(const reel &arg)
{
	reel res(arg.get_dim1(), arg.get_dim2(), arg.get_dim3());
	for(int i=0; i<arg.get_dim1(); i++)
		for(int j=0; j<arg.get_dim2(); j++)
			for(int z=0; z<arg.get_dim3(); z++)
				res(i, j, z) = exp(arg(i, j, z));
	return res;
}

reel sin(const reel &arg)
{
	reel res(arg.get_dim1(), arg.get_dim2(), arg.get_dim3());

	for(int i=0; i<arg.get_dim1(); i++)
		for(int j=0; j<arg.get_dim2(); j++)
			for(int z=0; z<arg.get_dim3(); z++)
				res(i, j, z) = sin(arg(i, j, z));
	return res;
}

float max(const reel &arg)
{
	return arg.max();
}

reel abs(const reel &arg)
{
	reel res(arg.get_dim1(), arg.get_dim2(), arg.get_dim3());
        for(int i=0; i<arg.get_dim1(); i++)
                for(int j=0; j<arg.get_dim2(); j++)
                        for(int z=0; z<arg.get_dim3(); z++)
                                res(i, j, z) = fabs(arg(i, j, z));
	return res;
}

reel operator-(const reel &arg)
{
	reel res(arg.t1, arg.t2, arg.t3);
	for(int i=0; i<arg.tot; i++)
		res(i) = -arg(i);
	return res;
}

reel operator*(const float cte, const reel &arg) //const
{
	return arg * cte;
}

reel PdtVect3D(const reel& a, const reel& b)
{
	if( a.get_dim2() != 0 || a.get_dim3() != 0 ||
		b.get_dim2() != 0 || b.get_dim3() != 0
	  )
		throw std::string("La fonction ne s'applique qu'aux vecteurs.");
	if( a.get_dim1() != b.get_dim1() )
		throw std::string("Les vecteurs n'ont pas les mêmes dimensions.");
	if( a.get_dim1() != 3 )
		throw std::string("Le produit vectoriel n'est ici défini que pour un espace 3D.");

	reel res(a.get_dim1());

	res(0) = a(1)*b(2) - a(2)*b(1);
	res(1) = a(2)*b(0) - a(0)*b(2);
	res(2) = a(0)*b(1) - a(1)*b(0);

	return res;
}
