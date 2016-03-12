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
import socket
import multiprocessing

HOST = 'localhost'    # The remote host
PORT = 8001           # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    msg = bytes(input(">>:"), encoding = "utf8")
    s.sendall(msg)
    data = s.recv(1024)
    #print(data)

    print('Received : %s' %str(data, encoding = 'utf8'))
s.close()

