#include "OGLCube.hpp"

#include <iostream>

namespace OGLCube {
    OGLCube::OGLCube(void): vertices(0), indices(0), rouge(0), vert(0), bleu(0), taille(1.0)
    {
        //        QString a = "Shaders/couleurs.vert";
        //        QString b = "Shaders/couleurs.frag";
        //        std::cerr << a.toStdString() << ", " << b.toStdString() << std::endl;
        //        m_program.addShaderFromSourceFile(QOpenGLShader::Vertex, a);
        //        std::cerr << m_program.log().toStdString() << std::endl;
        //        m_program.addShaderFromSourceFile(QOpenGLShader::Fragment, b);
        //        std::cerr << m_program.log().toStdString() << std::endl;
        init();
    }

    OGLCube::OGLCube(float t, std::string VerticeShader, std::string FragShader): vertices(0), indices(0), rouge(0), vert(0), bleu(0), taille(t)
    {
        //            m_program.addShaderFromSourceFile(QOpenGLShader::Vertex, QString(VerticeShader.c_str()));
        //            m_program.addShaderFromSourceFile(QOpenGLShader::Fragment, QString(FragShader.c_str()));
        init();
    }

    void OGLCube::init(void)
    {
        // Vertices
        /* Vertex 0 */      /* Vertex 1 */     /* Vertex 2 */    /* Vertex 3 */
        float tvertices[] = {-taille, -taille, -taille,   taille, -taille, -taille,   taille, taille, -taille,   -taille, taille, -taille,
            /* Vertex 4 */      /* Vertex 5 */     /* Vertex 6 */    /* Vertex 7 */
            -taille, -taille, taille,    taille, -taille, taille,    taille, taille, taille,    -taille, taille, taille};
        // Indices
        /*Triangle 1*/     /*Triangle 2*/
        unsigned int tindices[] = {  0, 1, 2,		2, 3, 0,  // Face 1
            5, 1, 2,           2, 6, 5,  // Face 2
            0, 1, 5,		5, 4, 0,  // Face 3
            4, 5, 6,		6, 7, 4,  // Face 4
            0, 4, 7,		7, 3, 0,  // Face 5
            7, 6, 2,		2, 3, 7}; // Face 6
        // Couleurs
        float trouge[] = {1.0, 0.0, 0.0,   1.0, 0.0, 0.0,   1.0, 0.0, 0.0,   1.0, 0.0, 0.0,   1.0, 0.0, 0.0,   1.0, 0.0, 0.0,   1.0, 0.0, 0.0,   1.0, 0.0, 0.0};
        float tvert[]  = {0.0, 1.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 0.0};
        float tbleu[]  = {0.0, 0.0, 1.0,   0.0, 0.0, 1.0,   0.0, 0.0, 1.0,   0.0, 0.0, 1.0,   0.0, 0.0, 1.0,   0.0, 0.0, 1.0,   0.0, 0.0, 1.0,   0.0, 0.0, 1.0};

        unsigned int N = 3 * 8;
        vertices = new float[N];
        for(unsigned int i = 0; i < N; i++)
            vertices[i] = tvertices[i];

        N = 6 * 2 * 3;
        indices = new unsigned int[N];
        for(unsigned int i = 0; i < N; i++)
            indices[i]  = tindices[i];

        N = 8 * 3;
        bleu  = new float[N];
        rouge = new float[N];
        vert  = new float[N];
        for(unsigned int i = 0; i < N; i++)
        {
            rouge[i] = trouge[i];
            bleu[i]  = tbleu[i];
            vert[i]  = tvert[i];
        }
    }

    OGLCube::~OGLCube(void)
    {
        delete[] indices;
        delete[] vertices;

        delete[] bleu;
        delete[] vert;
        delete[] rouge;
    }

    void OGLCube::Show(QGLShaderProgram &m_program, OGLMatrice::OGLMatrice &proj, OGLMatrice::OGLMatrice &model)
    {
        // Sauvegarde de la matrice :
        model.push();

        m_program.removeAllShaders();
        std::cerr << "OGLCube.cpp:" << __LINE__ << " " << m_program.log().toStdString() << std::endl;
        m_program.addShaderFromSourceFile(QGLShader::Vertex, QString("Shaders/couleurs.vert"));
        std::cerr << "OGLCube.cpp:" << __LINE__ << " " << m_program.log().toStdString() << std::endl;
        //m_program.addShaderFromSourceFile(QGLShader::Fragment, QString("Shaders/couleurs.frag"));
        std::cerr << "OGLCube.cpp:" << __LINE__ << " " << m_program.log().toStdString() << std::endl;
        /* ***** Commande nécessaire au rendu ***** */
        // Activation du shader
        if( !m_program.link() )
        {
            std::cerr << "OGLCube.cpp:" << __LINE__ << " " << m_program.log().toStdString() << std::endl;
            throw std::runtime_error("Shader do not want to link");
        }
        //glUseProgram(shader.getProgramID());
        m_program.bind();

        //glEnableVertexAttribArray(0);
        //glEnableVertexAttribArray(1);

        int   vloc = m_program.attributeLocation("in_Vertex")
            , mloc = m_program.uniformLocation("modelview")
            , ploc = m_program.uniformLocation("projection")
            , cloc = m_program.attributeLocation("in_Color")
            ;

        /* ***** Rendu ***** */
        // On envoie les matrices au shader
        // Envoi des vertices
        m_program.enableAttributeArray(vloc);
        m_program.enableAttributeArray(cloc);
        m_program.setAttributeArray(vloc, vertices, 3);
        //glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, vertices);

        m_program.setUniformValueArray( mloc, (GLfloat*)model.GetValues(), 4, 4);
        m_program.setUniformValueArray( ploc, (GLfloat*)proj.GetValues(), 4, 4);

        // Envoi de la couleur
        // Face 1
        m_program.setAttributeArray(cloc, rouge, 3);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, indices);

        // Face 2
        m_program.setAttributeArray(cloc, vert, 3);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, &indices[6]);

        // Face 3
        m_program.setAttributeArray(cloc, bleu, 3);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, &indices[12]);

        // Face 4
        m_program.setAttributeArray(cloc, rouge, 3);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, &indices[18]);

        // Face 5
        m_program.setAttributeArray(cloc, vert, 3);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, &indices[24]);

        // Face 6
        m_program.setAttributeArray(cloc, bleu, 3);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, &indices[30]);

        // Désactivation du shader et des tableaux
        m_program.disableAttributeArray(vloc);
        m_program.disableAttributeArray(cloc);

        m_program.release();

        // Restauration de la matrice
        model.pop();
    }

#ifdef TEXTURE_ACTIVATE
    OGLTexturedCube::OGLTexturedCube(void) : OGLCube(1.0, "Shaders/texture.vert", "Shaders/texture.frag"), texture("Textures/Caisse.jpg"), texture_coord(0)
    {
    }

    OGLTexturedCube::OGLTexturedCube(float t, std::string VerticeShader, std::string FragShader, std::string text) : OGLCube(t, "Shaders/texture.vert", "Shaders/texture.frag"), texture(text), texture_coord(0)
    {
    }
#endif
} /* OGLCube */
