#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

from joker.cast import syntax


def test_path_formatters():
    vals = [
        syntax.format_class_path(dict),
        syntax.format_function_path(dict.pop),
        syntax.format_function_path(lambda: 1),
    ]
    for v in vals:
        print(v)


if __name__ == '__main__':
    test_path_formatters()
