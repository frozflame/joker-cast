#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
from joker.cast.numeric import (
    numsys_cast,
    numsys_revcast,
)


def test_numsys_cast():
    num = 12341234
    base = 237
    idigits, fdigits = numsys_cast(num, base)
    assert num == numsys_revcast(base, idigits, fdigits)
