#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import os
import sys


def under_home_dir(*paths):
    if sys.platform == 'win32':
        homedir = os.environ["HOMEPATH"]
    else:
        homedir = os.path.expanduser('~')
    return os.path.join(homedir, *paths)


def under_package_dir(package, *paths):
    p_dir = os.path.dirname(package.__file__)
    return os.path.join(p_dir, *paths)
