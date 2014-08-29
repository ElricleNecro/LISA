#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from .Texture import Texture


def _chess(side, step):
    chess = np.zeros((side, side), dtype=np.uint32)
    for i in range(side):
        for j in range(step):
            chess[i, j:j+8:8] = 255
    return chess


class TextureManager(object):
    """
    A class to manage all the texture used in the program, avoiding the copy of
    unnecessary data in the memory of the graphic card.
    """

    def __init__(self, parent):
        """
        Initialize the manager and put a default texture in the database.
        """

        self.database = dict()
        self.parent = parent

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):

        # check that the parent can set the current context opengl
        if not hasattr(parent, "makeCurrent"):
            raise AttributeError(
                "The parent must have a method to set the current context."
            )
            return

        self._parent = parent

    def _makeCurrent(self):
        self.parent.makeCurrent()

    def loadTexture(self, filename, *args, **kwargs):
        """
        Given a texture file name, returns the texture if already loaded, else
        load the texture in the GPU memory.
        """

        # check the texture filename already loaded
        if filename in self.database:

            # return the texture
            return self.database[filename]

        # the texture is not in the database, so we load it
        else:

            # make the context current
            self._makeCurrent()

            # create the texture
            texture = Texture(*args, **kwargs)
            texture.loadImageFromFile(filename)
            texture.release()

            # store it in the database
            self.database[filename] = texture

            # return it
            return texture

    def remove(self, texture):
        """
        Remove a specified texture from the database.
        """

        if texture in self.database:
            # destroy the texture
            tmp = self.database[texture]
            del tmp

            # remove it from the database
            del self.database[texture]

    def __lshift__(self, textures):
        """
        Given a list of tuples of textures file names with their parameters in
        a dictionary, iteratively load them in the texture manager.
        """

        tex = []
        unit = 0
        for texture in textures:
            tmp = self.loadTexture(texture[0], **texture[1])
            tmp.unit = unit
            tex.append(tmp)
            unit += 1

        return tex

    def __del__(self):
        """
        Delete all textures in the database.
        """
        for texture in self.database.values():
            self.remove(texture)

# vim: set tw=79 :
