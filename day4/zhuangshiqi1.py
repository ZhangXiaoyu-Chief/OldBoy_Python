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
def login(func):
    def inner(*args, **kwargs):
        print('passed user verification...')
        return func(*args, **kwargs)
    return inner

def home(name):
    print('Welcome [%s] to home page' %name)
@login
def tv(name, passwd):
    print('Welcome [%s] to tv page' %name)
    print(passwd)
    return 4
def movie(name):
    print('Welcome [%s] to movie page' %name)

if __name__ == '__main__':
    print(tv('zhangxiaoyu', 123))