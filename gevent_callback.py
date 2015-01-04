#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuande Liu <miracle (at) gmail.com>
# gevent's rawlink(callback) are executed before gevent.join() return

from __future__ import print_function
import gevent
from gevent.pool import Pool
p = Pool(100)

alist = []

def return_self(x):
    return x

def callback(greenlet):
    """
    If we call `gevent.sleep(0)` in this callback:
        AssertionError: Impossible to call blocking function in the event loop callback
    """
    global alist
    alist.append( greenlet.value )
    2**2**20 # about 2s in Intel i5 2.4GHz

def run():
    for x in xrange(10000):
        b = p.spawn(return_self, x)
        b.rawlink(callback)

    global alist
    print('before join alist: {}'.format(len(alist)))
    p.join()
    print('after join alist: {}'.format(len(alist)))


run()
print('alist: {}'.format(len(alist)))

# before join alist: 9900
# after join alist: 10000
# alist: 10000
