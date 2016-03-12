#!/usr/bin/env python3
# coding:utf-8
'''
Created on:

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.1

Description:

Help:
'''

if __name__ == '__main__':
    import queue
    q = queue.PriorityQueue()
    q.put(1)
    q.put(3)
    q.put(2)
    print(q.get())
    print(q.get())
    print(q.get())