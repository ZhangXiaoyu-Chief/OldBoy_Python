#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月21日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: twisted字符串传输演示程序，服务端

Help:
'''
from twisted.internet import protocol
from twisted.internet import reactor

class Echo(protocol.Protocol): # 继承自protocol.Protocol
    '''
    Protocol描述了如何以异步的方式处理网络中的事件，这里继承protocol.Protocol是为了重写里面的一些方法
    Protocol包括如下方法，都可以在继承的基础上进行重写
    makeConnection               在transport对象和服务器之间建立一条连接
    connectionMade               连接建立起来后调用
    dataReceived                 接收数据时调用
    connectionLost               关闭连接时调用
    '''
    def dataReceived(self, data): # 重写dataReceived方法，当有数据过来的时候会执行该方法，data是收到的数据
        self.transport.write(data) # transport表示网络中两个通信节点之间的链接，write方法相当于往客户端发送消息

def main():
    factory = protocol.ServerFactory() # 定义服务端工厂类对象
    factory.protocol = Echo # 工厂对象的protcol等于我们刚才定义的类
    # reactor(反应堆)就是twisted的事件驱动，这是twisted的核心
    reactor.listenTCP(1234, factory) # 将服务端工厂类注册到reactor，也就是事件驱动的注册事件，第一个参数是端口，当reactor监测到该端口的状态，并根据状态触发相应的工厂类protocol的相关方法
    reactor.run() # 执行注册的事件，也即是事件驱动的启动监听
if __name__ == '__main__':
    main()