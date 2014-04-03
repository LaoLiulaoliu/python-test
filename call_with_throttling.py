#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuande Liu <miracle (at) gmail.com>
#
# Today I read my colleague's code, found call_with_throttling.
# Call_with_throttling is very tricky.
#
# 在刚开始的600次调用之前，由于smooth函数的作用，
# logs deque逐渐增长，而且随着队列增加而增长渐缓，
# 不过渐缓的十分平滑，肉眼分辨不出。
# 只要调用频率超过默认的0.1s每个，smooth函数就会起作用。
#
# 调用次数超过600之后，队列会因为wait_for_threshold而sleep，
# 稳定队列，保持600个，这样调用速率也稳定在0.1s每个了。
#
# 调整threshold_per_minute的大小，现象无太大变化。
#

from collections import deque
import time

def call_with_throttling(func, args=(), kwargs={}, threshold_per_minute=600):
    """ calling a func with throttling
    
    Throttling the function call with ``threshold_per_minute`` calls per minute.
    This is useful in case where the func calls a remote service having their throttling policy.
    We must honor their throttling, otherwise we will be banned shortly.

    :param func: the function to be called
    :param args: args of that function
    :param kwargs: kwargs of that function
    :param threshold_per_minute: defines how many calls can be made to the function per minute 
    """
    if not hasattr(call_with_throttling, 'logs'):
        call_with_throttling.logs = deque()
        call_with_throttling.started_at = time.time()
        call_with_throttling.count = 0
    logs = call_with_throttling.logs
    started_at = call_with_throttling.started_at
    call_with_throttling.count += 1
    count = call_with_throttling.count

    def remove_outdated():
        t = time.time()
        while True:
            if logs and logs[0] < t - 60:
                logs.popleft()
            else:
                break

    def wait_for_threshold():
        while len(logs) > threshold_per_minute:
            remove_outdated()
            time.sleep(0.3)

    def smoothen_calling_interval():
        average_processing_time = (time.time() - started_at) / count
        expected_processing_time = 60. / threshold_per_minute
        if expected_processing_time > average_processing_time:
#            time.sleep(0.1) # nearly have the same effect
            time.sleep((len(logs)+0.8)*expected_processing_time - len(logs)*average_processing_time)


    average_processing_time = (time.time() - started_at) / count
    expected_processing_time = 60. / threshold_per_minute
    print [expected_processing_time, average_processing_time], [count, len(logs)], time.time()-started_at

    if logs and len(logs) < threshold_per_minute:
        smoothen_calling_interval()
    else:
        wait_for_threshold()

    logs.append(time.time())
    return func(*args, **kwargs)


def app():
    return


# import Queue
# queue = Queue.Queue()
# list append is about 9 times faster than queue put
def generate_number(queue=[]):
    """ generate numbers in the range -2^63 ~ 2^63-1

    xrange or range can not take 2 ** 64 as a parameter.
    We cut all the numbers into 2 ** 20 (about 1 million) pieces.
    """
    begin = - 2 ** 63
    end = 2 ** 63 - 1
    step = 2 ** 43

    while begin < end:
        stop = begin + step
        if stop > end:
            stop = end
        # queue.put((begin, stop))
        queue.append((begin, stop))
        begin = stop
    return queue


def run():
    queue = generate_number()
    print 'generate numbers over.'

    while len(queue):
        # begin, end = queue.get()
        begin, end = queue.pop(0)
        for i in xrange(end - begin):
            call_with_throttling(app)


if __name__ == '__main__':
    run()
