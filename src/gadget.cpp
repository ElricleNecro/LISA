#include "gadget.hpp"

BadFile::BadFile(const std::string& error)
: msg(error)
{
}

BadFile::BadFile(const BadFile& error)
: msg(error.msg)
{
}

BadFile::~BadFile(void)
{
}

const char* BadFile::what(void) const noexcept
{
	return this->msg.c_str();
}

Gadget::Gadget(const std::string& fname, const int files)
: Data(fname), NbPart(0), _particle(nullptr), filename(fname), nb_files(files)
{
	this->Read(fname, files);
	this->RegenerateVertices();
}

Gadget::~Gadget(void)
{
	delete this->_particle;
}

void Gadget::Read(const std::string& fname, const int files)
{
	char buf[200];
	int dummy = 0;
	int pc_sph, n, pc_new, pc, ntot_withmasses, dummy2, k, i;
	FILE *fd = NULL;
	Particule P = nullptr;

#define SKIP fread(&dummy, sizeof(dummy), 1, fd);
#define SKIP2 fread(&dummy2, sizeof(dummy2), 1, fd);
#define TEST_SS2 if(dummy != dummy2) { fclose(fd); throw std::length_error("Wrong block size."); }

	for(i = 0, pc = 0; i < files; i++, pc = pc_new)
	{
		if(files > 1)
			sprintf(buf, "%s.%d", fname.c_str(), i);
		else
			sprintf(buf, "%s", fname.c_str());

		if(!(fd = fopen(buf, "r")))
			throw BadFile("Opening file '" + fname + "' has failed!");

		fread(&dummy, sizeof(dummy), 1, fd);
		fread(&this->header, sizeof(Header), 1, fd);
		fread(&dummy, sizeof(dummy), 1, fd);

		if(files == 1)
		{
			for(k = 0, this->NbPart = 0, ntot_withmasses = 0; k < 6; k++)
				this->NbPart += this->header.npart[k];
		}
		else
		{
			for(k = 0, this->NbPart = 0, ntot_withmasses = 0; k < 6; k++)
				this->NbPart += this->header.npartTotal[k];
		}

		for(k = 0, ntot_withmasses = 0; k < 6; k++)
		{
			if(this->header.mass[k] == 0)
				ntot_withmasses += this->header.npart[k];
		}

		if(i == 0)
		{
			P = new _particule_data[this->NbPart];
			//if( (P = malloc(this->NbPart * sizeof(struct _particule_data))) == NULL )
			if( P == nullptr || P == NULL )
			{
				fclose(fd);
				throw std::runtime_error("Allocation failed.");
			}
		}

		SKIP;
		for(k = 0, pc_new = pc; k < 6; k++)
		{
			for(n = 0; n < this->header.npart[k]; n++)
			{
				fread(&P[pc_new].Pos[0], sizeof(float), 3, fd);
				pc_new++;
			}
		}
		SKIP2;
		TEST_SS2;

		SKIP;
		for(k = 0, pc_new = pc; k < 6; k++)
		{
			for(n = 0; n < this->header.npart[k]; n++)
			{
				fread(&P[pc_new].Vit[0], sizeof(float), 3, fd);
				pc_new++;
			}
		}
		SKIP2;
		TEST_SS2;


		SKIP;
		for(k = 0, pc_new = pc; k < 6; k++)
		{
			for(n = 0; n < this->header.npart[k]; n++)
			{
				fread(&P[pc_new].Id, sizeof(int), 1, fd);
				pc_new++;
			}
		}
		SKIP2;
		TEST_SS2;


		if(ntot_withmasses > 0)
			SKIP;
		for(k = 0, pc_new = pc; k < 6; k++)
		{
			for(n = 0; n < this->header.npart[k]; n++)
			{
				P[pc_new].Type = k;

				if(this->header.mass[k] == 0)
				{
					fread(&P[pc_new].m, sizeof(float), 1, fd);
				}
				else
					P[pc_new].m = this->header.mass[k];
				pc_new++;
			}
		}
		if(ntot_withmasses > 0)
		{
			SKIP2;
			TEST_SS2;
		}


		if(this->header.npart[0] > 0)
		{
			SKIP;
			for(n = 0, pc_sph = pc; n < this->header.npart[0]; n++)
			{
				float tmp;
				fread(&tmp, sizeof(float), 1, fd);
				P[pc_sph].U = tmp;
				pc_sph++;
			}
			SKIP2;
			TEST_SS2;

			SKIP;
			for(n = 0, pc_sph = pc; n < this->header.npart[0]; n++)
			{
				float tmp;
				fread(&tmp, sizeof(float), 1, fd);
				P[pc_sph].Rho = tmp;
				pc_sph++;
			}
			SKIP2;
			TEST_SS2;

			if(this->header.flag_cooling)
			{
				SKIP;
				for(n = 0, pc_sph = pc; n < this->header.npart[0]; n++)
				{
					float tmp;
					fread(&tmp, sizeof(float), 1, fd);
					P[pc_sph].Ne = tmp;
					pc_sph++;
				}
				SKIP2;
				TEST_SS2;
			}
			else
				for(n = 0, pc_sph = pc; n < this->header.npart[0]; n++)
				{
					P[pc_sph].Ne = 1.0;
					pc_sph++;
				}
		}

		/*
		if( b_potential )
		{
			SKIP;
			float tmp;
			for(k = 0, pc_new = pc; k < 6; k++)
			{
				for(n = 0; n < header->npart[k]; n++)
				{
					fread(&tmp, sizeof(float), 1, fd);
					P[pc_new].Pot = tmp;
				}
			}
			SKIP2;
			TEST_SS2;
		}

		if( b_acceleration )
		{
			SKIP;
			float tmp[3];
			for(k = 0, pc_new = pc; k < 6; k++)
			{
				for(n = 0; n < header->npart[k]; n++)
				{
					fread(&tmp, sizeof(float), 3, fd);
					for(int j=0; j<3; j++) P[pc_new].Acc[j] = tmp[j];
					pc_new++;
				}
			}
			SKIP2;
			TEST_SS2;
		}

		if( b_rate_entropy && header->npart[0] > 0 )
		{
			SKIP;
			float tmp;
			for(n = 0, pc_sph = pc; n < header->npart[0]; n++)
			{
				fread(&tmp, sizeof(float), 1, fd);
				P[pc_sph].dAdt = tmp;
				pc_sph++;
			}
			SKIP2;
			TEST_SS2;
		}

		if( b_timestep )
		{
			SKIP;
			float tmp;
			for(k = 0, pc_new = pc; k < 6; k++)
			{
				for(n = 0; n < header->npart[k]; n++)
				{
					fread(&tmp, sizeof(float), 1, fd);
					P[pc_new].ts = tmp;
				}
			}
			SKIP2;
			TEST_SS2;
		}
		*/

		fclose(fd);
	}
#undef SKIP
#undef SKIP2
#undef TEST_SS2

	this->_particle = P;
}

void Gadget::RegenerateVertices(void)
{
	for(int i = 0; i < this->NbPart; i++)
	{
		this->vertices << QVector3D(this->_particle[i].Pos[0], this->_particle[i].Pos[1], this->_particle[i].Pos[2]);
		this->colors   << QVector3D(1, 0, 0);
	}
}

void Gadget::Show(QGLShaderProgram &m_program, QMatrix4x4 &model)
{
	m_program.setUniformValue( "modelview", model );
	m_program.setAttributeArray("in_Vertex", this->vertices.constData());
	m_program.setAttributeArray("in_Color", this->colors.constData());
	m_program.enableAttributeArray("in_Vertex");
	m_program.enableAttributeArray("in_Color");

	glDrawArrays(GL_POINTS, 0, this->vertices.size());
	//glDrawArrays(GL_TRIANGLES, 0, this->vertices.size());

	// Désactivation du shader et des tableaux
	m_program.disableAttributeArray("in_Vertex");
	m_program.disableAttributeArray("in_Color");
}
