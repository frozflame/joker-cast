#!/usr/bin/env python3
# coding: utf-8
import os
import re

from setuptools import setup, find_namespace_packages

# import joker; exit(1)
# DO NOT import your package from your setup.py


package_name = "cast"
description = "Type conversions"


def read(filename):
    with open(filename) as f:
        return f.read()


def version_find():
    root = os.path.dirname(__file__)
    path = os.path.join(root, "joker/{}/__init__.py".format(package_name))
    regex = re.compile(r"""^__version__\s*=\s*('|"|'{3}|"{3})([.\w]+)\1\s*(#|$)""")
    with open(path) as fin:
        for line in fin:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            mat = regex.match(line)
            if mat:
                return mat.groups()[1]
    raise ValueError("__version__ definition not found")


config = {
    "name": "joker-" + package_name,
    "version": version_find(),
    "description": "" + description,
    "keywords": "",
    "url": "https://github.com/frozflame/joker-cast",
    "author": "frozflame",
    "author_email": "frozflame@outlook.com",
    "license": "GNU General Public License (GPL)",
    "packages": find_namespace_packages(include=["joker.*"]),
    "namespace_packages": ["joker"],
    "zip_safe": False,
    "python_requires": ">=3.3",
    "install_requires": read("requirements.txt"),
    "classifiers": [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    # ensure copy static file to runtime directory
    "include_package_data": True,
    "long_description": read("README.md"),
    "long_description_content_type": "text/markdown",
}

setup(**config)
