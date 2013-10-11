#include "Shader.hpp"
#include <iostream>

namespace OpenGLShader {
	Shader::Shader(std::string vertexSource, std::string fragmentSource) : m_vertexSource(vertexSource), m_fragmentSource(fragmentSource), m_vertexID(0), m_fragmentID(0), m_programID(0), m_initialise(false)
	{
	}

	Shader::Shader(Shader const &shader) : m_vertexSource(shader.m_vertexSource), m_fragmentSource(shader.m_fragmentSource), m_vertexID(0), m_fragmentID(0), m_programID(0), m_initialise(shader.m_initialise)
	{
		// On initialise le shader si le shader source est lui aussi initialisé
		if(m_initialise == true)
			initialiser();
	}

	Shader::~Shader()
	{
		detruire();
	}

	bool Shader::initialiser()
	{
		// Création des shaders
		if(initialiserTypeShader(m_vertexID, GL_VERTEX_SHADER, m_vertexSource) == false)
			return false;

		if(initialiserTypeShader(m_fragmentID, GL_FRAGMENT_SHADER, m_fragmentSource) == false)
			return false;

		// Création du program
		m_programID = glCreateProgram();

		glAttachShader(m_programID, m_vertexID);
		glAttachShader(m_programID, m_fragmentID);

		// Linkage du program
		bindAttribLocation();
		glLinkProgram(m_programID);

		// On vérifie que le link c'est bien passé
		GLint link(0);
		glGetProgramiv(m_programID, GL_LINK_STATUS, &link);

		if(link != GL_TRUE)
		{
			// Récupération de la taille de l'erreur
			GLint tailleErreur(0);
			char *erreur(NULL);

			glGetProgramiv(m_programID, GL_INFO_LOG_LENGTH, &tailleErreur);

			// Allocation de l'erreur
			erreur = new char[tailleErreur + 1];

			// Copie de l'erreur dans la chaine de caractères
			glGetProgramInfoLog(m_programID, tailleErreur, &tailleErreur, erreur);
			erreur[tailleErreur] = '\0';

			// Affichage de l'erreur
			std::cout << "Erreur lors du link du program : " << erreur << std::endl;

			// On retourne false
			delete[] erreur;
			return false;
		}

		// Tout s'est bien passée, on retourne true
		m_initialise = true;

		return true;
	}

	bool Shader::initialiserTypeShader(GLuint &shader, GLenum type, std::string const &source)
	{
		// Génération de l'objet OpenGL Shader

		if(type == GL_VERTEX_SHADER)
			shader = glCreateShader(type);

		else if(type == GL_FRAGMENT_SHADER)
			shader = glCreateShader(GL_FRAGMENT_SHADER);

		else
		{
			glDeleteShader(shader);
			return false;
		}


		// Ouverture du fichier source

		std::string codeSource, ligneCodeSource;
		std::ifstream fichierSource(source.c_str());


		// On test l'ouverture du fichier

		if(!fichierSource)
		{
			std::cout << "Erreur le fichier : " << source << " n'existe pas" << std::endl;
			glDeleteShader(shader);

			return false;
		}


		// Si le fichier existe et qu'il est ouvert, alors on peut lire son contenu

		while(getline(fichierSource, ligneCodeSource))
		{
			codeSource += ligneCodeSource + '\n';
		}

		fichierSource.close();

		std::cout << codeSource << std::endl;


		// Compilation du shader

		GLint erreurCompilation(0), tailleErreur(0);
		const GLchar* chaineCodeSource = codeSource.c_str();

		glShaderSource(shader, 1, &chaineCodeSource, NULL);
		glCompileShader(shader);


		// Vérification de la compilation

		glGetShaderiv(shader, GL_COMPILE_STATUS, &erreurCompilation);

		if(erreurCompilation != GL_TRUE)
		{
			// Récupération de la taille de l'erreur

			glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &tailleErreur);


			// Allocation d'une chaine de caractères

			char *erreur = new char[tailleErreur + 1];
			erreur[tailleErreur] = '\0';


			// Récupération de l'erreur

			glGetShaderInfoLog(shader, tailleErreur, &tailleErreur, erreur);


			// Affichage de l'erreur

			std::cout << "Erreur de compilation du shader (" << type << ") " << erreur << std::endl;


			// On libère la mémoire et on retourne false

			delete[] erreur;
			return false;
		}


		// Tout s'est bien passé on retourne true

		return true;
	}

	void Shader::bindAttribLocation()
	{
		// Verrouillage des entrées Shader
		glBindAttribLocation(m_programID, 0, "in_Vertex");
		glBindAttribLocation(m_programID, 1, "in_Color");
		glBindAttribLocation(m_programID, 2, "in_TexCoord0");
		glBindAttribLocation(m_programID, 3, "in_Normal");
	}

	void Shader::detruire()
	{
		// Destruction des objets OpenGL
		glDeleteShader(m_vertexID);
		glDeleteShader(m_fragmentID);
		glDeleteProgram(m_programID);


		// RAZ des valeurs

		m_vertexID = 0;
		m_fragmentID = 0;
		m_programID = 0;
		m_initialise = false;
	}

	Shader& Shader::operator=(Shader const &shader)
	{
		// Si le shader à copier n'est pas lui-même

		if(this != &shader)
		{
			// Copie des sources

			m_vertexSource = shader.m_vertexSource;
			m_fragmentSource = shader.m_fragmentSource;
			m_initialise = shader.m_initialise;


			// Destruction du shader actuel

			detruire();


			// Initialisation du nouveau shader

			initialiser();
		}

		return *this;
	}

	GLuint Shader::getProgramID() const
	{
		return m_programID;
	}
}
