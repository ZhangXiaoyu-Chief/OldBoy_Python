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
    import socket
    ip_port = ('127.0.0.1', 9000)

    sk = socket.socket()
    sk.connect(ip_port)

    sk.sendall(bytes('你好', 'utf8'))
    server_reply = sk.recv(1024)
    print(str(server_reply, 'utf8'))
    while True:
        user_input = input(">> ").strip()
        sk.send(bytes(user_input, 'utf8'))
        server_reply = sk.recv(1024)
        print(str(server_reply, 'utf8'))

    sk.close()
