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
from libs import mylib


ip_port = ('127.0.0.1',9999)
sk = socket.socket()
sk.connect(ip_port)

data = mylib.b2s(sk.recv(100))
print(data)
while True:
    user_input = input(">> ").strip()
    if len(user_input) == 0: continue
    if user_input == 'q': break

    sk.sendall(mylib.s2b(user_input))
    server_ack_msg = mylib.b2s(sk.recv(100))
    cmd_res_msg = server_ack_msg.split('|')
    print('server respone:', server_ack_msg)
    if cmd_res_msg[0] == "CMD_RESULT_SIZE":
        cmd_res_size = int(cmd_res_msg[1])
        sk.send(b"CLIENT_READY_TO_RECV")
    res = ''
    received_size = 0
    print(cmd_res_msg)
    while received_size < cmd_res_size:
        data = sk.recv(500)
        received_size += len(data)
        print(data)
        #data = str(data.decode())
        res += str(data.decode())
    else:
        print(res)
        print('---recv done-----')

sk.close()