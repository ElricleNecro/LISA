#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ["ShadersNotLinked", "ShaderCompileError"]


class ShadersNotLinked(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class ShaderCompileError(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return "{0}".format(self._msg)


# vim: set tw=79 :
