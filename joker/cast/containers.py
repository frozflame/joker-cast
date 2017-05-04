#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import collections
import itertools

import six

from joker.cast.numeric import ceil


class DefaultOrderedDict(collections.OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
                not isinstance(default_factory, collections.Callable)):
            raise TypeError('first argument must be a callable')
        collections.OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return collections.OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()


class Circular(object):
    def __init__(self, iterable):
        self._items = list(iterable)
        assert self._items

    def __repr__(self):
        c = self.__class__.__name__
        return '{}({})'.format(c, self._items)

    def ix_turn(self, ix):
        if ix is None:
            return
        return len(self._items) - 1 - ix

    def ix_shift(self, *indexes):
        m = min(i for i in indexes if i is not None)
        if m >= 0:
            return indexes
        n = len(self._items)
        shift = ceil(-1. * m / n) * n
        new_indexes = []
        for ix in indexes:
            if ix is None:
                new_indexes.append(None)
            else:
                new_indexes.append(ix + shift)
        return tuple(new_indexes)

    def standardize(self, slc):
        """
        :param slc: a slice instance 
        :return: (start, stop, step)  # a tuple  
        """
        assert isinstance(slc, slice)
        if slc.step is None or slc.step >= 0:
            return self.ix_shift(slc.start, slc.stop, slc.step)
        return self.ix_shift(
            self.ix_turn(slc.start),
            self.ix_turn(slc.stop),
            -slc.step)

    def __getitem__(self, key):
        n = len(self._items)
        if isinstance(key, six.integer_types):
            return self._items[key % n]

        if isinstance(key, slice):
            start, stop, step = self.standardize(key)
            if key.step and key.step < 0:
                c_items = itertools.cycle(self._items[::-1])
            else:
                c_items = itertools.cycle(self._items)
            return itertools.islice(c_items, start, stop, step)


class CircularString(object):
    def __init__(self, string):
        self._string = string
        self._circular = Circular(string)

    def __repr__(self):
        c = self.__class__.__name__
        return '{}({})'.format(c, self._string)

    def __getitem__(self, key):
        return ''.join(list(self._circular[key]))
