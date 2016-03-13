#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 

Description: 
Help:
'''

if __name__ == '__main__':
    from redis_helper import RedisHelper

    obj = RedisHelper()
    while True:
        obj.public(input('>> '))