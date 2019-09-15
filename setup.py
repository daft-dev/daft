#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import re
import sys

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

dirname = os.path.dirname(os.path.realpath(__file__))
vre = re.compile('__version__ = "(.*?)"')
m = open(os.path.join(dirname, "daft.py")).read()
version = vre.findall(m)[0]

with open(os.path.join(dirname, "requirements.txt"), "r") as f:
    install_requires = f.read().splitlines()

setup(
    name="daft",
    version=version,
    description="PGM rendering at its finest",
    long_description=open("README.rst").read(),
    author="Daft Developers",
    author_email="danfm@nyu.edu",
    url="http://daft-pgm.org",
    py_modules=["daft"],
    package_data={"": ["LICENSE.rst", "README.rst"]},
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
