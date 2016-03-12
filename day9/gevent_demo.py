#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 

Description: 
Help:
'''
import gevent

def foo():
    print('running in foo')
    gevent.sleep(1)
    print('explicit contest to foo')
def bar():
    print('explicit in bar')
    gevent.sleep(2)
    print('context switch back to bar')

def ex():
    print('explicit in ex')
    gevent.sleep(1)
    print('context switch back to ex')
if __name__ == '__main__':
    gevent.joinall([
        gevent.spawn(foo),
        gevent.spawn(bar),
        gevent.spawn(ex),
    ])