#!/usr/bin/env python

from setuptools import setup


setup(
    name="daft",
    use_scm_version=True,
    description="PGM rendering at its finest",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="Daft Developers",
    author_email="danfm@nyu.edu",
    url="http://daft-pgm.org",
    py_modules=["daft"],
    install_requires=["matplotlib", "numpy", "setuptools"],
    extras_require={
        "test": ["pytest"],
        "docs": ["myst_nb", "sphinx", "jupytext"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
