#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from OpenGL import GL

__all__ = [
    "Buffer",
]


class Buffer(object, metaclass=ABCMeta):
    """
    A class to manage the creation and manipulation of buffer in OpenGL.
    """

    @abstractmethod
    def create(self):
        raise NotImplementedError("This essantial method must be implemented!")

    @abstractmethod
    def bind(self):
        raise NotImplementedError("This essantial method must be implemented!")

    @abstractmethod
    def release(self):
        raise NotImplementedError("This essantial method must be implemented!")

    @abstractmethod
    def delete(self):
        raise NotImplementedError("This essantial method must be implemented!")


# vim: set tw=79 :
