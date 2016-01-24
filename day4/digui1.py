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
def calc(n):
    res = n/2
    if res >1:
        res = calc(res)
        print(res)
    return n

if __name__ == '__main__':
    print(calc(10))