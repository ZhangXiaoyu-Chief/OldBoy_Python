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
import threading
import time
def addNum():
    global num
    print('--get num:', num)
    time.sleep(1)
    #lock.acquire()
    num += 1
    #lock.release()
    print(num)

if __name__ == '__main__':
    lock = threading.Lock()
    num = 0
    thread_list = []
    for i in range(100):
        t = threading.Thread(target = addNum)
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    print(num)