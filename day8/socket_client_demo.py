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
    sk = socket.socket()
    IP_PORT = ('127.0.0.1', 9999)
    sk.connect(IP_PORT)
    while True:
        msg = input('>> ').strip()
        if msg == 'quit':
            break
        if msg == '':
            continue
        sk.send(bytes(msg, 'utf8'))
        print(sk.recv(1024).decode())
    sk.close()