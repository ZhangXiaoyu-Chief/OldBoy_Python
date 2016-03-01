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
    sk.bind(ip_port)

    sk.listen(5)

    while True:
        print('server is waiting ...')
        conn, addr = sk.accept()

        client_data = conn.recv(1024)
        print(str(client_data, 'utf8'))
        conn.send(bytes('你是猪吗', 'utf8'))
        conn.close()
