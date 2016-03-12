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
import time
import threading, queue
q = queue.Queue()
def consumer(n):
    while True:

        print('consumer %stask  %s ' %(n, q.get()))
        time.sleep(1)
        q.task_done()

def producer(n):
    count = 1
    while True:
        print('生产者%s生产了一个包子' %n)
        q.put(count)
        count += 1
        q.join()
        print('生产者%s收到消息，所有的包子都卖完了' %n)




if __name__ == '__main__':
    c1 = threading.Thread(target = consumer, args = [1,])
    c2 = threading.Thread(target = consumer, args = [2,])
    c3 = threading.Thread(target = consumer, args = [3,])
    c4 = threading.Thread(target = consumer, args = [3,])

    p1 = threading.Thread(target = producer, args = [1,])
    p2 = threading.Thread(target = producer, args = [2,])


    c1.start()
    c2.start()
    c3.start()
    c4.start()

    p1.start()
    p2.start()