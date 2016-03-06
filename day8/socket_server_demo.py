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
import socketserver
class Myserver(socketserver.BaseRequestHandler):

    def handle(self):
        print('New Conn: ',self.client_address)
        while True:
            data = self.request.recv(1024)
            print('Client say: %s' %data.decode())
            self.request.send(data)


if __name__ == '__main__':
    IP_PORT = ('127.0.0.1', 9999)
    server = socketserver.ThreadingTCPServer(IP_PORT, Myserver)
    server.serve_forever()