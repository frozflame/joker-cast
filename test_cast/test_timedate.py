#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import datetime

from joker.cast.timedate import (
    TimeSlicer, sexagesimal_format, sexagesimal_parse,
)


def test_timeslicer():
    dts = [datetime.datetime.now()]
    for dt in dts:
        tms = TimeSlicer()
        tms.convert_datetime_to_timeslice(dt, relative=False)


def test_sexagesimal():
    assert isinstance(sexagesimal_parse('11'), int)
    assert isinstance(sexagesimal_parse('11.'), float)
    assert isinstance(sexagesimal_parse('11.0'), float)
    assert sexagesimal_format(61, 0) == '11'
    assert sexagesimal_format(61., 0) == '11.'
    assert sexagesimal_format(61., 1) == '11.0'


if __name__ == '__main__':
    test_sexagesimal()
    test_timeslicer()
