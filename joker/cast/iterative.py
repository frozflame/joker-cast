#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import itertools
from collections import deque
from functools import wraps
from itertools import chain, combinations

import six
from six import moves as six_moves

from joker.cast.numeric import ceil


# numpy is slow to load, don't add here


def chunkwize(chunksize, iterable):
    """
    >>> list(chunkwize(5, range(14)))
    [[0, 1, 2, 3, 4], 
     [5, 6, 7, 8, 9], 
     [10, 11, 12, 13]]
     
    :param chunksize: integer
    :param iterable:
    """
    chunksize = int(chunksize)
    chunk = []
    for item in iterable:
        if len(chunk) >= chunksize:
            yield chunk
            chunk = []
        chunk.append(item)
    yield chunk


def chunkwize_parallel(chunksize, *sequences):
    """
    >>> s1 = '1234567890'
    >>> s2 = 'abcdefghijk'
    >>> list(chunkwize_parallel(4, s1, s2))
    [['1234', 'abcd'], ['5678', 'efgh'], ['90', 'ijk']]
    
    :param chunksize: integer
    :param sequences: tuple of strings or lists (must support slicing!)
    """
    chunksize = int(chunksize)
    for i in itertools.count(0):
        r = [s[i * chunksize:(i + 1) * chunksize] for s in sequences]
        if any(r):
            yield r
        else:
            raise StopIteration


def all_combinations(iterable):
    """
    >>> list(all_combinations('abcd'))
    [(),
     ('a',),
     ('b',),
     ('c',),
     ('d',),
     ('a', 'b'),
     ('a', 'c'),
     ('a', 'd'),
     ('b', 'c'),
     ('b', 'd'),
     ('c', 'd'),
     ('a', 'b', 'c'),
     ('a', 'b', 'd'),
     ('a', 'c', 'd'),
     ('b', 'c', 'd'),
     ('a', 'b', 'c', 'd')]
    """
    items = list(iterable)
    return chain.from_iterable(
        combinations(items, i) for i in range(1 + len(items)))


def window_sum(wsize, numbers):
    """
    >>> numbers = [1, 10, 100, 1000, 10000, 100000]
    >>> list(window_sum(3, numbers))
    [111, 1110, 11100, 111000]
    
    :param wsize: integer, size of the moving window
    :param numbers: an iterable of numbers
    :return: a numpy.ndarray
    """
    queue = deque(maxlen=wsize)
    for num in numbers:
        queue.append(num)
        if len(queue) >= wsize:
            yield sum(queue)


_void = object()


def alternate(*iterables, fill=_void):
    """
    >>> ''.join(list(alternate('ABCD', 'abcde')))
    'AaBbCcDde'
    >>> ''.join(list(alternate('ABCD', 'abcde', fill='_')))
    'AaBbCcDd_e' 
    """
    zip_longest = six_moves.zip_longest
    alt = itertools.chain(*zip_longest(*iterables, fillvalue=fill))
    for item in alt:
        if item is not _void:
            yield item


class Circular(object):
    """
    >>> c = Circular([0, 1, 2, 3, 4]) 
    >>> list(c[-1:5])
    [4, 0, 1, 2, 3, 4]
    """
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
    """
    >>> cs = CircularString('0123456789')
    >>> cs[-1:12]
    '9012345678901'
    """
    def __init__(self, string):
        self._string = string
        self._circular = Circular(string)

    def __repr__(self):
        c = self.__class__.__name__
        return '{}({})'.format(c, self._string)

    def __getitem__(self, key):
        return ''.join(list(self._circular[key]))


# TODO: suport negative index (castfunc=-1 to get last item)
def castable(func):
    """
    >>> @castable
    ... def myfunc(*args):
    ...     for i in range(*args):
    ...         yield i
    ...
    >>> myfunc(12, castfunc=tuple)
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    >>> myfunc(0, 12, 2, castfunc=2)
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
   
    Purely syntax sugar,
    to make interactive use of some functions easier.
    Cast a generator function to list, set, or select n-th item, etc.

        myfunc(..., castfunc=list)   <=>  list(myfunc(...))
        myfunc(..., castfunc=1)      <=>  list(myfunc(...))[1]
    """
    @wraps(func)
    def _decorated_func(*args, **kwargs):
        castfunc = None
        if 'castfunc' in kwargs:
            castfunc = kwargs['castfunc']
            del kwargs['castfunc']

            # shortcut to pick up nth record
            if isinstance(castfunc, int):
                n = castfunc
                castfunc = lambda result: next(itertools.islice(result, n, None))

        result = func(*args, **kwargs)
        if castfunc:
            result = castfunc(result)
        return result
    return _decorated_func
