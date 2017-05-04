#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function
import inspect


def fmt_class_path(obj):
    if isinstance(obj, type):
        klass = obj
    else:
        klass = type(obj)
    m = getattr(klass, '__module__', None)
    q = getattr(klass, '__qualname__', None)
    n = getattr(klass, '__name__', None)
    name = q or n or ''
    if m:
        return '{}.{}'.format(m, name)
    return name


def deprecated_fmt_class_path(klass):
    if not isinstance(klass, type):
        raise TypeError('must be a new-style class')
    if klass.__module__ == '__main__':
        prefix = ''
    else:
        prefix = klass.__module__ + '.'
    return prefix + klass.__name__


def fmt_function_path(func):
    if not inspect.ismethod(func):
        mod = getattr(func, '__module__', None)
        if mod is None:
            return func.__qualname__
        else:
            return '{}.{}'.format(mod, func.__qualname__)
    klass_path = fmt_class_path(func.__self__)
    return '{}.{}'.format(klass_path, func.__name__)


def instanciate(cls):
    return cls()


def instanciate_with_foolproof(cls):
    """
    The return class can be called again without error
    """
    if '__call__' not in cls.__dict__:
        cls.__call__ = lambda x: x
    return cls()


class AttrEchoer(object):
    """
    Resembles an enum type
    Reduces typos by using syntax based completion of dev tools
    
    Example:
        
        @instanciate_with_foolproof
        class Event(AttrEchoer):
            _prefix = 'event'
            bad_params = ''  # assign whatever
            unauthorized_access = ''  
            undefined_fault = ''
            ...
       
        # no error: 
        assert Event.unauthoried  == 'event.bad_params'
    """
    _prefix = '_root.'

    def __init__(self):
        pass

    def __getattribute__(self, key):
        kls = type(self)
        if key in kls.__dict__ and key != '_prefix':
            if not kls._prefix:
                return key
            return '{}{}'.format(kls._prefix, key)
        return object.__getattribute__(self, key)

