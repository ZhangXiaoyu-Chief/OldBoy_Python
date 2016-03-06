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
def sayhi(num):
    print('%s is say hi' %num)
    import time
    time.sleep(5)
import threading
if __name__ == '__main__':
    t1 = threading.Thread(target = sayhi, args = [1, ])
    t2 = threading.Thread(target = sayhi, args = [2, ])
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(t1.getName())
    print(t2.getName())