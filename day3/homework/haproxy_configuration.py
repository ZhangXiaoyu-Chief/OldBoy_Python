#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2015年12月29日

@author: 张晓宇

Email: 61411916@qq.com

Version: 

Description: 

Help:
'''
from model.haproxy import haproxy

if __name__ == '__main__':
    haproxy = haproxy('haproxy.conf')
    print(haproxy.get_backend() )
