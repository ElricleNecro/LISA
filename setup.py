#! /usr/bin/env python3
# -*- coding:Utf8 -*-

#--------------------------------------------------------------------------------------------------------------
# All necessary import:
#--------------------------------------------------------------------------------------------------------------
import os, sys, glob

try:
	import numpy
except ImportError:
	print("Numpy is a needed dependancy.")
	sys.exit(-1)

#from setuptools import find_packages
import setuptools as st
from distutils.core import setup
from distutils.command.install_data import install_data
from Cython.Distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

packages = st.find_packages()

#--------------------------------------------------------------------------------------------------------------
# Setup for the cython part:
#--------------------------------------------------------------------------------------------------------------

## Needed function:
def scandir(dir, files=[]):
	for file in os.listdir(dir):
		path = os.path.join(dir, file)
		if os.path.isfile(path) and path.endswith(".pyx"):
			files.append(path.replace(os.path.sep, ".")[:-4])
		elif os.path.isdir(path):
			scandir(path, files)
	return files

def makeExtension(extName, **kwargs):
	extPath = [ extName.replace(".", os.path.sep)+".pyx" ]
	return Extension(
			extName,
			extPath
		)

## Setup:
extNames = scandir("LISA")

extensions = []
for name in extNames:
	extensions.append(
		makeExtension(
			name,
			cython_directives = {
				"embedsignature" : True,
			}
		)
	)

#--------------------------------------------------------------------------------------------------------------
# Call the setup function:
#--------------------------------------------------------------------------------------------------------------
setup(
	name         = 'LISA is a Simulation Analyzer',
	version      = '0.1a',
	description  = 'Python Module for analysis simulation.',
	author       = 'Guillaume Plum, Manuel Duarte',			# Sûrement pas bon, à changer.

	cmdclass     = {'install_data': install_data, 'build_ext': build_ext},

	packages     = packages,
	package_data = {'LISA': glob.glob('Shaders/*') + glob.glob('Textures/*')},
	ext_modules  = cythonize(
				extensions,
				include_path = ['.']
			),
)

#vim:spelllang=
