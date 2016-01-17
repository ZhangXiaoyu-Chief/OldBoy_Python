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






