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
class Mythreading(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        print('%s is say hi' %self.num)
        import time
        time.sleep(5)

if __name__ == '__main__':
    t1 = Mythreading(1)
    t2 = Mythreading(2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(t1.getName())
    print(t2.getName())
