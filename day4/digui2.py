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
def func(arg1, arg2, stop):
    if arg1 == 0:
        print(arg1)
        print(arg2)
    arg3 = arg1 + arg2
    print(arg3)
    if arg3 < stop:
        func(arg2, arg3, stop)

if __name__ == '__main__':
    func(0, 1, 30)