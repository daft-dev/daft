#!/usr/bin/env python


try:
    from setuptools import setup, Extension
    setup, Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
    setup, Extension

import os
import sys

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

sys.path.append(os.path.dirname(__file__))

import daft


setup(
    name="daft",
    version=daft.__version__,
    author="David W. Hogg & Daniel Foreman-Mackey",
    author_email="danfm@nyu.edu",
    py_modules=["daft"],
    description="PGM rendering at its finest.",
    long_description=open("README.rst").read(),
    install_requires=[
                        "numpy",
                        "matplotlib"
                     ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
