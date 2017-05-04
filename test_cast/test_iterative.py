#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

from string import digits

from joker.cast.iterative import CircularString


def test_circular_string():
    cs = CircularString(digits)
    for i in range(101):
        s = cs[:i]
        assert len(s) == i


if __name__ == '__main__':
    test_circular_string()
