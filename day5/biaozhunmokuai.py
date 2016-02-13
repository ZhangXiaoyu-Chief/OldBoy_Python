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
import json
if __name__ == '__main__':
    # print(time.clock())
    # print(time.process_time())
    # print(time.time())
    # print(time.ctime())
    # print(time.gmtime())
    # print(time.localtime())
    # print(time.mktime(time.localtime()))
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print(time.strptime("2016-01-30 18:20:40", "%Y-%m-%d %H:%M:%S"))
    #
    # print(datetime.date.today())
    # print(datetime.datetime.fromtimestamp(time.time()))
    #
    # # print(random.random())
    # # for i in range(10):
    # #     sys.stdout.write('>>')
    # #     sys.stdout.flush()
    # #     time.sleep(random.random())
    #
    # today = list(time.localtime())
    # today[3:] = [0,0,0,0,0,0]
    # print(time.mktime(tuple(today)))
    # today2 = today
    # today2[1] -=1
    # print(today)
    # print(time.mktime(tuple(today)))
    # print(time.mktime(tuple(today2)))
    import codecs

    #with codecs . open ( path , 'w' , 'utf-8' ) as w :
    test = '中文测试'
    # with codecs.open('testjson.txt', 'r' , 'utf-8' ) as f:
    #     ttt = json.load(f)
    # print(ttt)
    # with codecs.open('testjson.txt', 'r', 'utf-8') as f:
    #     print(json.load(f))
    with codecs.open('testjson.txt', 'w', 'utf-8') as f:
        json.dump(test, f, ensure_ascii = False )




