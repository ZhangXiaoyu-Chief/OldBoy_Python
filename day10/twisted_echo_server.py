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
from twisted.internet import protocol
from twisted.internet import reactor

class Echo(protocol.Protocol): # 集成自
    def dataReceived(self, data): # 重写dataReceived方法，当有数据过来的时候会执行该方法，data是收到的数据
        self.transport.write(data) # transport

def main():
    factory = protocol.ServerFactory() # 定义服务端工厂类
    factory.protocol = Echo
    # reactor就是twisted的事件驱动
    reactor.listenTCP(1234,factory) # 将服务段工厂类注册到reactor
    reactor.run() # 执行注册的事件
if __name__ == '__main__':
    main()