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
import sys
import socket
import time
import gevent

from gevent import socket,monkey
monkey.patch_all()
def server(port):
    s = socket.socket() # 创建服务端socket对象
    s.bind(('0.0.0.0', port)) # 绑定端口
    s.listen(500) # 同时可以有500访问
    while True:
        cli, addr = s.accept()
        gevent.spawn(handle_request, cli)

def handle_request(s):
    try:
        while True:
            data = s.recv(1024)
            print("recv:", data)
            s.send(data)
            if not data:
                s.shutdown(socket.SHUT_WR) # 向客户端发送断开连接请求，如果客户端已经断开，则无用

    except Exception as  ex:
        print(ex)
    finally:

        s.close()
if __name__ == '__main__':
    server(8001)