#!/usr/bin/env python
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description:

Help:
'''
def foo1():
    print('foo1')
def foo2(arg):
    print(arg)
def foo3(arg1, arg2):
    print(arg1, arg2)
def foo4(arg1, arg2 = 'ok'):
    print(arg1, arg2)

def foo5(*args):
    print(args, type(args))

def foo6(**kwargs):
    print(kwargs, type(kwargs))

def foo7(arg1, arg2 = 1, *args, **kwargs):
    print(arg1, arg2, args, kwargs)

def foo8(*args, **kwargs):
    print(args, kwargs)

def Foo2(arg1, arg2 = 123, ):
    print(arg1, arg2)
def Foo3(*args):
    print(args)

def Foo4(**kwargs):
    print(kwargs, type(kwargs))

def Foo5(arg1, arg2 = 'abc', *args, **kwargs):
    print('arg1:', arg1)
    print('arg2:', arg2)
    print('args', args)
    print('kwargs', kwargs)
def Foo6():
    print('start')
    return None
    print('end')

def Foo7():
    return 123, 'abc'

def Foo8(*args, **kwargs):
    print(args)
    print(kwargs)
if __name__ == '__main__':
    foo1()
    foo2('foo2')
    foo3('foo3','good')
    foo4('foo4')
    foo4('foo4','no ok')
    foo3(arg2 = 'good too', arg1 = 'foo3' )

    foo5(1, 2, 3)
    foo6(k1 = 1, k2 = 2, k3 = 3)
    foo7(1, 3, 2, 3, k1 = 4, k2 = 5)
    li = [11, 22, 33, 44]
    dic = {'k1':'value1', 'k2': 'value2'}
    foo8(li, dic)
    foo8(*li, **dic)


    s1 = "{0} is {1}"
    li = ['Python', 'good']
    print(s1.format(*li))
    s2 = "{name} is {acter}"
    dic = {'name':'Python', 'acter':'good'}
    print(s2.format(**dic))

    la = lambda x: x+1
    print(la(1))
    Foo2('abc')
    Foo2('abc', 345)

    Foo3(1, 2, 'abc')
    Foo4(k1 = 'abc', k2 = 123)

    Foo5(123, 'bcd', 123, 'abc', k1 = 123, k2 = 'abc')
    f = lambda r: 3.14 * r * r
    print(f(4))

    print(Foo6())

    res1, res2 = Foo7()
    print('res1:', res1)
    print('res2:', res2)

    res = Foo7()
    print('res:', res)

    li = [1, 2, 3]
    dic = {'k1':1, 'k2':2}
    Foo8(li, dic)
    Foo8(*li, **dic)










