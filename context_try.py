#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuande Liu <miracle (at) gmail.com>

import contextlib
from contextlib import contextmanager

@contextmanager
def make_context():
    try:
#        for i in [3/3, 9, 2/1]:
#            yield i
        yield 5
    except:
        raise ValueError("bad error.")
    else:
        print '0h, else'
    finally:
        print '  finally'

with make_context() as e:
    print 'out', [e]
print

class Context(object):

    def __init__(self, handle_error):
        print '__init__(%s)' % handle_error
        self.handle_error = handle_error

    def __enter__(self):
        print '__enter__()'
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print '__exit__(%s, %s, %s)' % (exc_type, exc_val, exc_tb)
        return self.handle_error

with Context(True):
    raise RuntimeError('error message handled')

print

with Context(False):
    raise RuntimeError('error message propagated')
