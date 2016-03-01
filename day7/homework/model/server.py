#!/usr/bin/env python
# coding:utf-8
import socketserver
class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        conn.sendall(bytes('欢迎使用65ftp','utf8'))

        flag = True
        while flag:
            data = conn.recv(1024)
            print(data)
            if data == 'exit':
                flag = False
            elif data == '0':
                conn.sendall('1111')
            else:
                conn.sendall('2222')

class myftp(object):
    def __init__(self):
        self.__server = socketserver.ThreadingTCPServer(('127.0.0.1', 9999), Myserver)

    def runserver(self):
        self.__server.serve_forever()