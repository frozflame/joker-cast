#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import datetime

from joker.cast.timedate import TimeSlicer


def test_timeslicer():
    dts = [datetime.datetime.now()]
    for dt in dts:
        tms = TimeSlicer()
        tms.convert_datetime_to_timeslice(dt, relative=False)


