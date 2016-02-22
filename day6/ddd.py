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
import shelve

d = shelve.open('shelve_test') #打开一个文件

class Test(object):
    def __init__(self,n):
        self.n = n


t = Test(123)
t2 = Test(123334)

name = ["alex","rain","test"]
d["test"] = name #持久化列表
d["t1"] = t      #持久化类
d["t2"] = t2

d.close()