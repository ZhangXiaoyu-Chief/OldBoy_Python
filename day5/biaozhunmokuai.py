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
import time
import datetime
import random
import sys
if __name__ == '__main__':
    print(time.clock())
    print(time.process_time())
    print(time.time())
    print(time.ctime())
    print(time.gmtime())
    print(time.localtime())
    print(time.mktime(time.localtime()))
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(time.strptime("2016-01-30 18:20:40", "%Y-%m-%d %H:%M:%S"))

    print(datetime.date.today())
    print(datetime.datetime.fromtimestamp(time.time()))

    print(random.random())
    for i in range(10):
        sys.stdout.write('>>')
        sys.stdout.flush()
        time.sleep(random.random())



