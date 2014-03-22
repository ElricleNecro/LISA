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

packages = st.find_packages()

#--------------------------------------------------------------------------------------------------------------
# Call the setup function:
#--------------------------------------------------------------------------------------------------------------
print(glob.glob('Shaders/*') + glob.glob('Textures/*'))
setup(
	name        = 'LISA is a Simulation Analyzer',
	version     = '0.1a',
	description = 'Python Module for analysis simulation.',
	author      = 'Guillaume Plum, Manuel Duarte',			# Sûrement pas bon, à changer.

	cmdclass    = {'install_data': install_data},

	packages    = packages,
	package_data={'LISA': glob.glob('Shaders/*') + glob.glob('Textures/*')},

	#data_files  = [
		#('share/LibThese/animation-plugins', ["share/LibThese/animation-plugins/__init__.py"]), #glob.glob("share/LibThese/animation-plugins/*.py")),
	#],
	#scripts = [
		#'scripts/animationv2.py'
	#],
)
