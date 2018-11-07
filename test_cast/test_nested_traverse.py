#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

from zlib import adler32
from joker.cast.nested.traverse import Traverser


testdata = {
    'n2733': 'x32', 'n2735': 'x34', 'n2742': 'x44', 'n2744': 'x46',
    'n2745': 'x47', 'n2747': 'x49', 'n2748': 'x50', 'n2749': 'x51'}


def t1():
    travr = Traverser(testdata, print)
    travr.traverse()


class CK(object):
    def __init__(self):
        self.value = None

    def consume(self, data):
        data = data.encode('ascii')
        if self.value is None:
            self.value = adler32(data)
        else:
            self.value = adler32(data, self.value)


def test_traverse():
    for x in range(1000):
        ck = CK()
        # m = hashlib.md5()
        # travr = Traverser(testdata, lambda x: None)
        # travr = Traverser(testdata, lambda x: m.update(x.encode('ascii')))
        travr = Traverser(testdata, ck.consume)
        travr.traverse()


if __name__ == '__main__':
    # test_traverse()
    t1()


