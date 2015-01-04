#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Another Event wait and set test:
# http://stackoverflow.com/questions/20418339/is-it-a-bug-of-the-wait-method-of-gevent-event-event

import random
 
import gevent
from gevent.event import AsyncResult
 
 
class TestAsyncResult(object):
    def __init__(self):
        self.event = AsyncResult()
 
    def run(self):
        producers = [gevent.spawn(self._producer, i) for i in xrange(3)]
        consumers = [gevent.spawn(self._consumer, i) for i in xrange(3)]
        tasks     = []
        tasks.extend(producers)
        tasks.extend(consumers)
        gevent.joinall(tasks)
 
    def _producer(self, pid):
        print("I'm producer %d and now I don't want consume to do something" % (pid,))
        sleeptime = random.randint(5, 10) * 0.01
        print("Sleeping time is %f" % (sleeptime, ))
        gevent.sleep(sleeptime)
        print("I'm producer %d and now consumer could do something." % (pid,))
        self.event.set('producer pid %d' % (pid, ))
        
    def _consumer(self, pid):
        print("I'm consumer %d and now I'm waiting for producer" % (pid,))
        gevent.sleep(random.randint(0, 5) * 0.01)
        value = self.event.wait()
        print("I'm consumer %d. Value is %r and now I can do something" % (pid, value))
 
 
if __name__ == '__main__':
    test = TestAsyncResult()
    test.run()
