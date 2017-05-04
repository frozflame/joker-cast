#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

from joker.cast import syntax
from joker.cast.serialize import JSONEncoderExtended, human_json_dumps


@syntax.instanciate_with_foolproof
class Event(syntax.AttrEchoer):
    prefix = 'event'
    unauthorized = ''  # assign whatever
    undefined_fault = ''


def test_path_formatters():
    vals = [
        syntax.fmt_class_path(dict),
        syntax.fmt_class_path(Event),
        syntax.fmt_class_path(JSONEncoderExtended),
        syntax.fmt_function_path(dict.pop),
        syntax.fmt_function_path(JSONEncoderExtended.default),
        syntax.fmt_function_path(human_json_dumps),
        syntax.fmt_function_path(lambda: 1),
    ]
    for v in vals:
        print(v)


if __name__ == '__main__':
    test_path_formatters()
