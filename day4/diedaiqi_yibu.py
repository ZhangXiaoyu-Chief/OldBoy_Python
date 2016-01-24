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
if __name__ == '__main__':
    import time
    def consumer(name):
        print('%s 准备吃包子' %name)
        while True:
            baozi = yield # 通过yield实现传递参数，此时consumer阻塞在这里，直到执行了send()方法，将参数传递过来，并复制给变量

            print("包子[%s]来了，被[%s]吃了！" %(baozi, name))

    def producer(name):
        c = consumer('A')
        c2 = consumer('B')
        c.__next__()
        c2.__next__()
        print('老子开始准备吃包子了')
        for i in range(10):
            time.sleep(1)
            print('做了2个包子')
            c.send(i)
            c2.send(i)

    producer('zhangxiaoyu')