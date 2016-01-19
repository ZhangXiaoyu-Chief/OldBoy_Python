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
if __name__ == '__main__':
    print(abs(-1))
    print(all([1, True, 1 == 1]))
    print(any([None, "", [], (), {}]))
    print(bin(10))
    print(bool([]))
    enu = enumerate(['abc', 'def', 'ghi'])
    print(enu)
    for i in enu:
        print(i)
    print(list(enu))