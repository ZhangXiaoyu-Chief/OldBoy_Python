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
from model.client import ftpclient
if __name__ == '__main__':
    myclient = ftpclient()
    myclient.start()