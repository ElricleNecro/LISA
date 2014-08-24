#! /usr/bin/env python3
# -*- coding:Utf8 -*-

# --------------------------------------------------------------------------------------------------------------
# All necessary import:
# --------------------------------------------------------------------------------------------------------------
import os
import sys
import glob

try:
    import numpy
except ImportError:
    print("Numpy is a needed dependancy.")
    sys.exit(-1)

# from setuptools import find_packages
import setuptools as st
from distutils.core import setup
from distutils.command.install_data import install_data
from Cython.Distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

packages = st.find_packages()

# --------------------------------------------------------------------------------------------------------------
# Setup for the cython part:
# --------------------------------------------------------------------------------------------------------------


def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files


def makeExtension(extName, test=False, **kwargs):
    """
    Create an extension for Cython with the path for the
    directory in which .pyx files are presents.
    """
    extPath = [extName.replace(".", os.path.sep) + ".pyx"]
    cfile = extName.split(".")
    dir = os.path.join(*cfile[:-1])
    cfile = glob.glob(os.path.join(dir, "c*.c"))
    extPath += cfile

    opt_dict = dict(
        include_dirs=["."],   # adding the '.' to include_dirs is CRUCIAL!!
        extra_compile_args=["-std=c99"],
        extra_link_args=['-g'],
        libraries=[],
        cython_include_dirs=[
            os.path.join(
                os.getenv("HOME"),
                '.local/lib/python' + ".".join(
                    [str(a) for a in sys.version_info[:2]]
                ) + '/site-packages/Cython/Includes'
            )
        ]
    )

    for key in kwargs.keys():
        if key in opt_dict:
            opt_dict[key] += kwargs[key]
        else:
            opt_dict[key] = kwargs[key]

    if test:
        return extPath, opt_dict
    else:
        return Extension(
            extName,
            extPath,
            **opt_dict
        )

# Setup:
extNames = scandir("LISA")

extensions = []
for name in extNames:
    extensions.append(
        makeExtension(
            name,
            cython_directives={
                "embedsignature": True,
            }
        )
    )

# --------------------------------------------------------------------------------------------------------------
# Call the setup function:
# --------------------------------------------------------------------------------------------------------------
setup(
    name='LISA is a Simulation Analyzer',
    version='0.1a',
    description='Python Module for analysis simulation.',
    author='Guillaume Plum, Manuel Duarte',
    cmdclass={
        'install_data': install_data,
        'build_ext': build_ext
    },
    packages=packages,
    include_package_data=True,
    package_data={
        'LISA': [
            "Data/Shaders/heightmap/*.*sh",
            "Data/Shaders/sprite/*.*sh",
            "Data/Shaders/halo/*.*sh",
            "Data/Shaders/rippler/*.*sh",
            "Data/Shaders/widget/*.*sh",
            "Data/Shaders/reader/mock/*.*sh",
            'Data/Shaders/*.*sh',
            'Data/Textures/heightmap/*.png',
        ]
    },
    ext_modules=cythonize(
        extensions,
        include_path=['.']
    ),
)

# vim:spelllang=
