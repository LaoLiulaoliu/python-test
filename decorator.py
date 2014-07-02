#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reference: http://www.cnblogs.com/rhcad/archive/2011/12/21/2295507.html

''' 对带参数的函数进行装饰，
    内嵌包装函数的形参和返回值与原函数相同，装饰函数返回内嵌包装函数对象
'''
def deco(func):
    def _deco(a, b):
        print("before myfunc() called.")
        ret = func(a, b)
        print("  after myfunc() called. result: %s" % ret)
        return ret
    return _deco
 
@deco
def myfunc(a, b):
    print(" myfunc(%s,%s) called." % (a, b))
    return a + b
 
#myfunc(1, 2)
#myfunc(3, 4)


''' 对参数数量不确定的函数进行装饰，
    参数用(*args, **kwargs)，自动适应变参和命名参数
'''
def deco(func):
    def _deco(*args, **kwargs):
        print("before %s called." % func.__name__)
        ret = func(*args, **kwargs)
        print("  after %s called. result: %s" % (func.__name__, ret))
        return ret
    return _deco
 
@deco
def myfunc1(a, b):
    print(" myfunc1(%s,%s) called." % (a, b))
    return a+b
 
@deco
def myfunc2(a, b, c):
    print(" myfunc2(%s,%s,%s) called." % (a, b, c))
    return a+b+c
 
#myfunc1(1, 2)
#myfunc1(3, 4)
#myfunc2(1, 2, 3)
#myfunc2(3, 4, 5)



''' 让装饰器带参数， 和上一示例相比在外层多了一层包装。
    装饰函数名实际上应更有意义些
'''
def deco(arg):
    def _deco(func):
        def __deco():
            print("before %s called [%s]." % (func.__name__, arg))
            func()
            print("  after %s called [%s]." % (func.__name__, arg))
        return __deco
    return _deco
 
@deco("module1")
def myfunc():
    print(" myfunc() called.")
 
@deco("module2")
def myfunc2():
    print(" myfunc2() called.")
 
#myfunc()
#myfunc2()







class mylocker(object):
    def __init__(self):
        print("mylocker.__init__() called.")
         
    @staticmethod
    def acquire():
        print("mylocker.acquire() called.")
         
    @staticmethod
    def unlock():
        print("  mylocker.unlock() called.")
 
class lockerex(mylocker):
    @staticmethod
    def acquire():
        print("lockerex.acquire() called.")
         
    @staticmethod
    def unlock():
        print("  lockerex.unlock() called.")
 
def lockhelper(cls):
    '''cls 必须实现acquire和release静态方法'''
    def _deco(func):
        def __deco(*args, **kwargs):
            print("before %s called." % func.__name__)
            cls.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                cls.unlock()
        return __deco
    return _deco


class example(object):
    @lockhelper(mylocker)
    def myfunc(self):
        print(" myfunc() called.")
 
    @lockhelper(mylocker)
    @lockhelper(lockerex)
    def myfunc2(self, a, b):
        print(" myfunc2() called.")
        return a + b
 
if __name__=="__main__":
    a = example()
    print(a.myfunc())
    print ('&'*80)
    print(a.myfunc2(1, 2))
    print(a.myfunc2(3, 4))
