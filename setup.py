#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "music-tag-names",
    version = "0.1",
    packages = find_packages(),

    install_requires = ['mutagen>=1.29']
)

