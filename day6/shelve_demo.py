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
sw = shelve.open('shelve_test.pkl') # 创建shelve对象

name = ['13', '14', '145', 6] # 创建一个列表
dist_test = {"k1":"v1", "k2":"v2"}
sw['name'] = name # 将列表持久化保存
sw['dist_test'] = dist_test
sw.close() # 关闭文件，必须要有

sr = shelve.open('shelve_test.pkl')
print(sr['name']) # 读出列表
print(sr['dist_test']) # 读出字典
sr.close()

