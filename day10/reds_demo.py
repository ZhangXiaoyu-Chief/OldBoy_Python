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
import redis
if __name__ == '__main__':
    r = redis.Redis(host = '127.0.0.1')
    print(r.keys())
    r.set('Name', 'sanjiang')
    print(r.get('Name'))