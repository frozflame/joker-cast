#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import json

from joker.cast.nested.tree import (
    get_parent_from_ascendants,
    compact_tree_assemble,
    compact_tree_disemble,
    standard_tree_dissemble,
    standard_tree_assemble,
)

testdata = [
    {'id': 1, 'parent': 0},
    {'id': 11, 'parent': 1},
    {'id': 12, 'parent': 1},
    {'id': 13, 'parent': 1},
    {'id': 111, 'parent': 11},
    {'id': 112, 'parent': 11},
    {'id': 121, 'parent': 12},
    {'id': 122, 'parent': 12},
    {'id': 123, 'parent': 12},
    {'id': 133, 'parent': 13},
    # {'id': 8, 'parent': 4},
]


def demo(data):
    print(json.dumps(data, indent=4))
    return data


def demo_standard_tree_assemble():
    tree, tmap = standard_tree_assemble(testdata)
    return demo(tree)


def demo_compact_tree_assemble():
    tree, tmap = compact_tree_assemble(testdata)
    return demo(tree)


def test_standard_tree_assemble():
    tree, tmap = standard_tree_assemble(testdata)
    dissembled = standard_tree_dissemble(tree['children'][0])
    for rec in dissembled:
        ascendants = [0] + rec['ascendants']
        rec['parent'] = ascendants[-1]

    test_lines = ['{id}:{parent}'.format(**r) for r in testdata]
    diss_lines = ['{id}:{parent}'.format(**r) for r in dissembled]
    test_lines.sort()
    diss_lines.sort()
    for a, b in zip(test_lines, diss_lines):
        assert a == b
        # print(a, b)


def test_compact_tree_assemble():
    tree, tmap = compact_tree_assemble(testdata)
    dissembled = compact_tree_disemble(tree)
    for rec in dissembled:
        rec['parent'] = get_parent_from_ascendants(rec['ascendants'])

    test_lines = ['{id}:{parent}'.format(**r) for r in testdata]
    diss_lines = ['{id}:{parent}'.format(**r) for r in dissembled]
    test_lines.sort()
    diss_lines.sort()
    for a, b in zip(test_lines, diss_lines):
        assert a == b
        # print(a, b)


if __name__ == '__main__':
    test_standard_tree_assemble()
    test_compact_tree_assemble()
    t1 = demo_standard_tree_assemble()
    t2 = demo_compact_tree_assemble()
