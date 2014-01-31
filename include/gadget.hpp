#ifndef GADGET_H

#define GADGET_H

#include <stdio.h>

#include <fstream>
#include <iostream>
#include <exception>
#include <stdexcept>

#include "interface.hpp"

class BadFile : public std::exception {
	public:
		BadFile(const std::string& error);
		BadFile(const BadFile& error);
		virtual ~BadFile(void) noexcept;

		virtual const char* what(void) const noexcept;

	private:
		std::string msg;
};

typedef struct io_header
{
	int		npart[6];                       /*!< number of particles of each type in this file */
	double		mass[6];                      	/*!< mass of particles of each type. If 0, then the masses are explicitly
							       stored in the mass-block of the snapshot file, otherwise they are omitted */
	double		time;                         	/*!< time of snapshot file */
	double		redshift;                     	/*!< redshift of snapshot file */
	int		flag_sfr;                       /*!< flags whether the simulation was including star formation */
	int		flag_feedback;                  /*!< flags whether feedback was included (obsolete) */
	unsigned int	npartTotal[6];          	/*!< total number of particles of each type in this snapshot. This can be
							       different from npart if one is dealing with a multi-file snapshot. */
	int		flag_cooling;                   /*!< flags whether cooling was included  */
	int		num_files;                    	/*!< number of files in multi-file snapshot */
	double		BoxSize;                      	/*!< box-size of simulation in case periodic boundaries were used */
	double		Omega0;                       	/*!< matter density in units of critical density */
	double		OmegaLambda;                  	/*!< cosmological constant parameter */
	double		HubbleParam;                  	/*!< Hubble parameter in units of 100 km/sec/Mpc */
	int		flag_stellarage;                /*!< flags whether the file contains formation times of star particles */
	int		flag_metals;                    /*!< flags whether the file contains metallicity values for gas and star particles */
	unsigned int	npartTotalHighWord[6];  	/*!< High word of the total number of particles of each type */
	int		flag_entropy_instead_u;         /*!< flags that IC-file contains entropy instead of u */
	char		fill[60];	                /*!< fills to 256 Bytes */
} Header;                               		/*!< holds header for snapshot files */

typedef struct _particule_data {
	float Pos[3];
	float Vit[3];
	float m;
	float Pot;
	float Acc[3];
	float dAdt;
	float ts;
	float Rho;
	float U;
	float Ne;
	int Id;
	int Type;
}*Particule;

class Gadget : public Data {
	public:
		Gadget(const std::string& fname, const int files = 1);
		Gadget(const Gadget& old);
		~Gadget(void);

		virtual void Show(QGLShaderProgram &m_program, QMatrix4x4 &model);

	private:
		Particule _particle;
		int NbPart;

		std::string filename;
		int nb_files;

		// Gadget Header
		Header header;

		// Vertices et indices
		QVector<QVector3D> vertices;
		QVector<QVector3D> colors;

		void RegenerateVertices(void);
		void Read(const std::string& fname, const int files);
};

#endif /* end of include guard: GADGET_H */
