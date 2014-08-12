#!/usr/bin/env python3
# -*- coding:Utf8 -*-

import os

# Directory in which all data are in:
PREFIX = os.path.join(os.path.dirname(__file__), "Data")

# Directory to place textures in:
TEXTURE_DIR = os.path.abspath(
    os.path.join(PREFIX, "Textures")
)

# Directory to place shaders in:
SHADERS_DIR = os.path.abspath(
    os.path.join(PREFIX, "Shaders")
)
