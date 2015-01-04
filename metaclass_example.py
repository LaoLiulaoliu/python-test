#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuande Liu <miracle (at) gmail.com>

class UpperAttrMetaclass(type):
    """ Class attributes which not start with '__',
        replace their name to uppercase.
    """
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)

        return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)

class Foo(object):
  __metaclass__ = UpperAttrMetaclass

  bar = 'bip'


print hasattr(Foo, 'bar')
# Out: False
print hasattr(Foo, 'BAR')
# Out: True

f = Foo()
print f.BAR
# Out: 'bip'


