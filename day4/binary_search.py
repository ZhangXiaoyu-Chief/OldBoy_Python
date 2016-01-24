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
'''
[0, 1, 2, 3]
[0, 1, 2, 3]
[0, 1, 2, 3]
[0, 1, 2, 3]

[0, 0, 0, 0]
[1, 1, 1, 1]
[2, 2, 2, 2]
[3, 3, 3, 3]
'''

def binary_search(data_source, find_n):
    le = len(data_source)
    mid = int(le/2)
    if le >= 1:
        if data_source[mid] > find_n:
            print('lift of %s' %data_source[mid])
            print(data_source[:mid])
            binary_search(data_source[:mid], find_n)
        elif data_source[mid] < find_n:
            print('right of %s' %data_source[mid])
            print(data_source[mid:])
            binary_search(data_source[mid:], find_n)
        else:
            print('find %s' %data_source[mid])
    else:
         print('not fountd')

if __name__ == '__main__':
    data = list(range(1, 100, 2))
    print(data)
    binary_search(data, 2)