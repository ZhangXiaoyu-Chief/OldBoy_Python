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
# This is the Twisted Get Poetry Now! client, version 3.0.

# NOTE: This should not be used as the basis for production code.

import optparse

from twisted.internet.protocol import Protocol, ClientFactory


def parse_args():
    '''
    获取并处理命令行选项和参数的函数
    :return: 返回选项和要传输的文件
    '''
    # 定义usage信息
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, Twisted version 3.0
Run it like this:

  python get-poetry-1.py port1 port2 port3 ...
"""

    parser = optparse.OptionParser(usage) # 定义optparse对象

    _, addresses = parser.parse_args() # 由于没有定义选项，所以只获取参数，前面的“_,”是个小技巧

    if not addresses: # 如果没有获取参数
        print(parser.format_help()) # 打印parser.format_help()返回的帮助信息也就是usage定义的信息
        parser.exit() # parser.exit()可以退出程序，并打印选项帮助信息

    def parse_address(addr): # 处理输入的参数
        '''
        处理ip和端口参数
        :param addr: ip和端口参数
        :return: 主机地址和端口
        '''
        if ':' not in addr: # 如果不包含:，说明只有地址
            host = '127.0.0.1' # 主机地址就是127.0.0.1
            port = addr # 端口等于参数
        else:
            host, port = addr.split(':', 1) # 获取用:分割的主机地址和端口

        if not port.isdigit(): # 判断端口是否是数字
            parser.error('Ports must be integers.') # 如果不是直接通过parser.error输出错误

        return host, int(port) # 返回的值和端口

    return map(parse_address, addresses) # 把输入的参数列表分别通过parse_address函数进行处理，返回正确的格式


class PoetryProtocol(Protocol):

    poem = '' # 初始化文件已经传输的文件内容为空

    def dataReceived(self, data): # 重写dataReceived方法
        self.poem += data # 拼接文件内容

    def connectionLost(self, reason): # 重写connectionLost方法
        self.poemReceived(self.poem) # 调用poemReceived方法，将已经接收的文件内容传过去

    def poemReceived(self, poem): # 在继承的基础上，自定义一个方法

        self.factory.poem_finished(poem) # 将接收的文件内容传递给工厂类的poem_finished方法，这个方法也是我们自定义的，而不是继承自工厂类的父类


class PoetryClientFactory(ClientFactory): # 定义工厂类，继承自ClientFactory

    protocol = PoetryProtocol # 定义工厂类的protocol

    def __init__(self, callback): # 重写构造方法
        self.callback = callback # 顶一个回调函数

    def poem_finished(self, poem): # 自定义一个方法poem_finished，参数为已经接收的文件内容
        self.callback(poem) # 执行自己的回调函数


def get_poetry(host, port, callback):
    '''
    获取服务端文件函数
    :param host: 服务端ip
    :param port: 服务端端口
    :param callback: 回调函数
    :return: 无
    '''
    """
    Download a poem from the given host and port and invoke

      callback(poem)

    when the poem is complete.
    """
    from twisted.internet import reactor
    factory = PoetryClientFactory(callback) # 定义工厂类，将回调函数传递个构造方法
    reactor.connectTCP(host, port, factory) # 启动将工厂类注册到reactor


def poetry_main():
    '''
    主函数
    :return: 无
    '''
    addresses = parse_args() # 调用parse_args函数处理命令行参数，获取地址列表

    from twisted.internet import reactor # 导入reactor

    poems = [] # 初始化一个变量，用来存储已经接收的文件内容，由于是一个客户端可以同时接收多个服务端的内容，所以一个列表

    def got_poem(poem): # 定义函数用来作为回调函数
        '''
        自定义的回调函数
        :param poem: 已经接收完的文件内容
        :return: 无
        '''
        poems.append(poem) # 将将接收到的文件内容追加到poems
        if len(poems) == len(addresses): # 如果已接收完文件内容的列表的成员各数等于地址列表，说明全部接收完了
            reactor.stop() # 关闭时间监听

    for address in addresses: # 遍历地址列表
        host, port = address # 获取地址和端口
        get_poetry(host, port, got_poem) # 执行分别执行get_poetry接收服务端的文件，将刚才定义的函数got_poem作为回调函数传递给get_poetry，并通过get_poetry在传递给工厂类

    reactor.run() # 启动事件监听

    for poem in poems: # 遍历poems
        print(poem) # 打印文件内容

if __name__ == '__main__':
    poetry_main()