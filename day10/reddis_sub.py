#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月22日

@author: 张晓宇

Email: 61411916@qq.com

Version: V1.0

Description: Redis订阅和发布演示程序，订阅方
Help:
'''

from redis_helper import RedisHelper # 导入redis公共类
if __name__ == '__main__':
    obj = RedisHelper() # 创建公共类对象
    redis_sub = obj.subscribe() # 执行收听方法

    while True:
        msg = redis_sub.parse_response() # 第二次调用parse_response()方法，开始阻塞知道收到一条消息
        print(msg) # 打印消息信息，parse_response()方法返回的其实是一个列表类似[b'message', b'fm104.5', b'abc']
