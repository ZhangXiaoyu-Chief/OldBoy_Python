#!/usr/bin/env python
# coding:utf-8
'''
Created on: 2016年2月27日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: socket演示程序，服务端

Help:
'''
if __name__ == '__main__':
    import socket                              # 导入socket模块
    ip_port = ('127.0.0.1', 9000)              # 定义监听端口和IP地址
    sk = socket.socket()                       # 创建socket对象
    sk.bind(ip_port)                           # 绑定IP地址和端口
    sk.listen(5)
    print('server is waiting ...')
    while True:
        conn, addr = sk.accept()               # 等待接收客户端请求，并返回客户端socket对象和客户端ip地址，此时是阻塞的，知道有链接进来，程序才会继续
        client_data = conn.recv(1024)          # 接收数据如果客户端没有发送数据过来，继续阻塞，直到有消息进来
        print(str(client_data, 'utf8'))
        conn.send(bytes('你是猪吗', 'utf8'))   # 向客户端发送消息
        conn.close()                           # 关闭连接