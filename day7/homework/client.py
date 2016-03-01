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
import socket


ip_port = ('127.0.0.1',9999)
sk = socket.socket()
sk.connect(ip_port)
sk.settimeout(5)

while True:
    data = sk.recv(1024)
    print('receive:',data)
    inp = input('please input:')
    sk.sendall(inp.encode('utf8'))
    if inp == 'exit':
        break

sk.close()