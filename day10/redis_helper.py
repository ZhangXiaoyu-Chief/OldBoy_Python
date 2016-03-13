#!/usr/bin/env python3
# coding:utf-8
import redis


class RedisHelper:

    def __init__(self):
        self.__conn = redis.Redis(host='127.0.0.1') # 定义reddis对象
        self.chan_sub = 'fm104.5'  # 订阅频道
        self.chan_pub = 'fm104.5' # 发布频道

    def public(self, msg): # 发布方法
        self.__conn.publish(self.chan_pub, msg) # 调用reddis对象的publish方法发布消息
        return True

    def subscribe(self): # 订阅消息方法
        pub = self.__conn.pubsub()  # 创建订读对象
        pub.subscribe(self.chan_sub) # 订阅频道
        pub.parse_response() # 开始订阅，第一次是不阻塞的，之后在调用这个方法就是阻塞的直到收到消息
        return pub # 返回订阅对象