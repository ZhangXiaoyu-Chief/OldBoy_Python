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
import optparse, os

from twisted.internet.protocol import ServerFactory, Protocol


def parse_args():
    '''
    获取并处理命令行选项和参数的函数
    :return: 返回选项和要传输的文件
    '''
    # 定义usage信息
    usage = """usage: %prog [options] poetry-file

This is the Fast Poetry Server, Twisted edition.
Run it like this:

  python fastpoetry.py <path-to-poetry-file>

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-server-1/fastpoetry.py poetry/ecstasy.txt

to serve up John Donne's Ecstasy, which I know you want to do.
"""

    parser = optparse.OptionParser(usage) # 定义optparse对象，optparse模块主要是用来处理命令行参数，usage表示当命令参数错误或没有参数的时候输出的内容

    help = "The port to listen on. Default to a random available port." # --port选项帮助信息
    parser.add_option('--port', type='int', help=help) # 添加--port选项，类型int，也就是该参数必须是整数类型

    help = "The interface to listen on. Default is localhost."  # --iface的帮助信息
    parser.add_option('--iface', help=help, default='localhost') # 添加--iface参数，也就是启动监听的IP地址，default表示默认值，这里默认是localhost

    options, args = parser.parse_args() # 调用parser.parse_args()返回定义好的选项和其他参数
    print("--arg:", options, args) # 打印选项和参数

    if len(args) != 1: # 如果没有参数，说明没有指定要文件，也就是要传输给客户端的文件
        parser.error('Provide exactly one poetry file.') # 输出错误parser.error方法会将信息输出到屏幕，并停止程序继续执行

    poetry_file = args[0] # 获取要传输给客户端的文件

    if not os.path.exists(args[0]): # 判断文件是否存在
        parser.error('No such file: %s' % poetry_file) # 如果不存在输出错误

    return options, poetry_file # 返回选项和要传输的文件


class PoetryProtocol(Protocol): # 定义protocol类，同样继承自twisted.internet.protocol.Protocol

    def connectionMade(self): # 重写了connectionMade方法，当连接建立之后执行
        self.transport.write(self.factory.poem) # self.factory.poem的内容发送到客户端，
        # 这里涉及到twisted的一个特性Protocol类的对象作为Factory类的成员，
        # 却可以通过self.factory获取他所属工厂类的东西
        # 说明工厂类和Protocol类是是互相映射的
        self.transport.loseConnection() # 关闭连接


class PoetryFactory(ServerFactory): # 定义server端工厂类，继承自ServerFactory

    protocol = PoetryProtocol # 定义工厂类的protocol

    def __init__(self, poem): # 重写构造方法
        self.poem = poem # self.poem等于传过来的参数，也就是文件内容


def main():
    options, poetry_file = parse_args() # 调用parse_args获取命令行选项和要传输的文件

    poem = open(poetry_file).read() # 读取要传输的文件，这里一次性读取出来，所以不适合非常大的文件

    factory = PoetryFactory(poem) # 定义工厂类，将文件内容作为参数传递给构造方法

    from twisted.internet import reactor # 导入reactor

    port = reactor.listenTCP(options.port or 9000, factory,
                             interface=options.iface) # 将工厂类主操到reactor，并返回端口号

    print('Serving %s on %s.' % (poetry_file, port.getHost())) # 打印消息

    reactor.run() # 启动事件监听

if __name__ == '__main__':
    main()