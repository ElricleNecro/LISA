#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ShadersNotLinked(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


# vim: set tw=79 :
