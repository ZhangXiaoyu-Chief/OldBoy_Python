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
def light():
    import time
    if not event.isSet():
        event.set()
    count = 0
    while True:
        if count < 10:
            print('\033[42;1m--green light on--\033[0m')
        elif count < 13:
            print('\033[43;1m--yellow light on--\033[0m')
        elif count < 20:
            if event.isSet():
                event.clear()
            print('\033[41;1m--red light on--\033[0m')
        else:
            count = 0
            if not event.isSet():
                event.set()
        time.sleep(1)
        count += 1

def car(n):
    import time
    while True:
        time.sleep(1)
        if event.isSet():
            print('car [%s] is running...' %n)
        else:
            print('car [%s] is waiting for the red light...' %n)
            event.wait()

if __name__ == '__main__':
    event = threading.Event()
    Light = threading.Thread(target = light)
    Light.start()
    for i in range(3):
        t = threading.Thread(target = car, args = [i,])
        t.start()