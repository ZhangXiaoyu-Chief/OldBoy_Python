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
def Before(request,kargs):
    print('before')

def After(request,kargs):
    print('after')


def Filter(before_func,after_func):
    def outer(main_func):
        def wrapper(request,kargs):

            before_func(request,kargs)

            main_func(request,kargs)

            after_func(request,kargs)

        return wrapper
    return outer

@Filter(Before, After)
def Index(request,kargs):
    print('index')


if __name__ == '__main__':
    Index(1,2)