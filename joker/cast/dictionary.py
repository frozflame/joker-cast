#!/usr/bin/env python3
# coding: utf-8

import warnings

from joker.cast.collective import DefaultOrderedDict, RecursiveDefaultDict, RecursiveCounter

warnings.warn(
    "import from joker.cast.collective instead",
    DeprecationWarning
)

_ = [
    DefaultOrderedDict,
    RecursiveDefaultDict,
    RecursiveCounter,
]
