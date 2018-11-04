#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import datetime

from joker.cast.timedate import (
    TimeSlicer, sexagesimal_format, sexagesimal_parse,
    smart_time_parse_to_seconds, time_format,
)


def test_timeslicer():
    dts = [datetime.datetime.now()]
    for dt in dts:
        tms = TimeSlicer()
        tms.convert_datetime_to_timeslice(dt, relative=False)


def check_chars():
    for i in range(60):
        c = sexagesimal_format(i, 0)
        if i < 10:
            assert ord(c) == i + ord('0')
            continue
        m, n = divmod(i - 10, 2)
        if n == 0:
            assert c.islower()
            assert ord(c) - ord('a') == m
        else:
            assert c.upper()
            assert ord(c) - ord('A') == m


def test_sexagesimal():
    check_chars()
    assert isinstance(sexagesimal_parse('11'), int)
    assert isinstance(sexagesimal_parse('11.'), float)
    assert isinstance(sexagesimal_parse('11.0'), float)
    assert sexagesimal_format(61, 0) == '11'
    assert sexagesimal_format(61., 0) == '11.'
    assert sexagesimal_format(61., 1) == '11.0'


def test_time_parse():
    # 1min 2sec
    assert smart_time_parse_to_seconds('2:3') == 123

    # 1hour 1min 2sec
    assert smart_time_parse_to_seconds('1:1:2') == 3662

    # 1hour 2sec
    assert smart_time_parse_to_seconds('1::2') == 3602

    # 1hour
    assert smart_time_parse_to_seconds('1::') == 3600

    # 1hour 1min 2sec
    assert smart_time_parse_to_seconds('10102') == 3662

    # 2min
    assert smart_time_parse_to_seconds('200') == 120


def test_time_format():
    assert len(time_format()) == 13


if __name__ == '__main__':
    test_sexagesimal()
    test_timeslicer()
    test_time_parse()
