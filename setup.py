#!/usr/bin/env python

from setuptools import setup

setup(
    name = "music-tag-names",
    version = "0.1",

    scripts = ["music_tag_names.py"],

    install_requires = ['mutagen>=1.29'],
)
