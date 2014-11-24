#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os

__all__ = [
    "getFontsFiles",
    "getDefaultFont",
]

FONT_DIRECTORIES = [
    "/usr/share/fonts/TTF/",
]


def getFontsFiles():

    # init the directory
    available = {}

    # loop over predefined directories
    for directory in FONT_DIRECTORIES:

        # get the list of files
        fonts = glob.glob(os.path.join(directory, "*.ttf"))

        # loop over font files
        for font in fonts:

            # get the basename of the file
            basename, _ = os.path.splitext(os.path.basename(font))

            # add it to available fonts
            available[basename] = font

    # return fonts
    return available


def getDefaultFont():

    # get available fonts
    fonts = getFontsFiles()

    # list of fonts
    fontNames = list(fonts.keys())
    fontNames.sort()

    return fonts[fontNames[0]]

# vim: set tw=79 :
