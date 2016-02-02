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
    data = [10,4,33,21,54,3,8,11,5,22,2,1,17,13,6]
    for i in range(1, len(data)):
        for j in range(len(data) - i):
            if data[j] > data[j + 1]:
                # tmp = data[j + 1]
                # data[j + 1] = data[j]
                # data[j] = tmp
                data[j], data[j + 1] = data[j + 1], data[j]
    print(data)