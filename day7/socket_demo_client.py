#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年2月27日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: socket演示程序，客户端

Help:
'''
import socket

if __name__ == '__main__':
    ip_port = ('127.0.0.1', 9000)       # 定义服务端ip地址和端口
    sk = socket.socket()                # 创建socket对象
    sk.connect(ip_port)                 # 连接服务端
    sk.sendall(bytes('你好', 'utf8'))   # 发送数据
    server_reply = sk.recv(1024)        # 接收数据
    print(str(server_reply, 'utf8'))
    sk.close()                          # 关闭连接
