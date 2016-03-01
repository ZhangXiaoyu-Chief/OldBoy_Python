#!/usr/bin/env python
# coding:utf-8
import socketserver
from libs import mylib
import subprocess
class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        print(self)
        conn = self.request
        conn.sendall(bytes('欢迎使用65ftp','utf8'))

        flag = True
        while flag:
            client_data = mylib.b2s(conn.recv(1024))
            if not client_data:break
            print('recv cmd:', client_data)
            cmd = client_data.strip()
            cmd_call = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
            cmd_result = cmd_call.stdout.read()
            if len(cmd_result) == 0:
                cmd_result = b"cmd execution has no ouput..."
            ack_msg = mylib.s2b("CMD_RESULT_SIZE|%s" %len(cmd_result))
            conn.sendall(ack_msg)
            client_ack = mylib.b2s(conn.recv(50))
            print(client_ack)
            if client_ack == 'CLIENT_READY_TO_RECV':
                conn.sendall(cmd_result)
                print(cmd_result)
        conn.close()



class myftp(socketserver.BaseRequestHandler):
    def __init__(self):
        self.__server = socketserver.ThreadingTCPServer(('127.0.0.1', 9999), Myserver)


    def runserver(self):
        print(self.__server)
        self.__server.serve_forever()