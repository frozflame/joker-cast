#!/usr/bin/env python3
# coding: utf-8

from joker.cast import regular_cast, smart_cast


def test_casting():
    assert regular_cast('2017', int) == 2017
    assert regular_cast('2017i', int) == '2017i'
    assert regular_cast('2017i', int, 0) == 0
    assert smart_cast('2017', 2016) == 2017
    assert smart_cast('2017i', 2016) == 2016
