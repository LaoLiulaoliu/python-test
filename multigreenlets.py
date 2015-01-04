#!/usr/bin/env python2.7
#coding: utf-8

import gevent
from gevent import Greenlet

class MyGreen(Greenlet):
    def __init__(self, timeout, msg):
        Greenlet.__init__(self)
        self.timeout = timeout        
        self.msg     = msg

    def _run(self):
        print("I'm from subclass of Greenlet and want to say: %s" % (self.msg,))
        gevent.sleep(self.timeout)
        print("I'm from subclass of Greenlet and done!")


class TestMultigreen(object):
    def __init__(self, timeout=0):
        self.timeout = timeout
        
    def run(self):
        green0 = gevent.spawn(self._task, 0, 'just 0 test')
        green1 = Greenlet.spawn(self._task, 1, 'just 1 test')
        green2 = MyGreen(self.timeout, 'just 2 test')
        green2.start()

        gevent.joinall([green0, green1, green2])
        print('Tasks done!')

    def _task(self, pid, msg):
        print("I'm task %d and want to say: %s" % (pid, msg))
        gevent.sleep(self.timeout)
        print("Task %d done." % (pid,))


if __name__ == '__main__':
    test = TestMultigreen()
    test.run()
