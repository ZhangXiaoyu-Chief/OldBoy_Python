#!/usr/bin/env python3
# coding:utf-8
import socketserver
from conf import conf
from model.users import users,user
from libs import mylib
import socket


class Myftphandle(socketserver.BaseRequestHandler):
    def handle(self):
        import os
        self.__loger = mylib.mylog(conf.LOGS, isstream = True)
        self.__current_user = user('guest', '', conf.DEFAULT_QUOTA)
        self.__home_path =  os.path.abspath(os.path.join(conf.HOME_PATH,self.__current_user.get_username()))
        self.__current_path = self.__home_path
        self.__code_list = conf.CODE_LIST
        self.__loger.info('Client %s:%s is connect the server' %self.client_address)
        while  True:
            try:
                data = mylib.b2s(self.request.recv(1024))
            except socket.error as e:
                self.__loger.info('Has lost client')
                break
            if not data:
                self.__loger.info('Has lost client')
                break     #如果收不到客户端数据了（代表客户端断开了），就断开
            self.instruction_allowcation(data) #客户端发过来的数据统一交给功能分发器处理

    def instruction_allowcation(self, instructions):
        instructions = instructions.split("|")
        function_str = instructions[0] # 客户端发过来的指令中,第一个参加都必须在服务器端有相应的方法处理
        if hasattr(self, function_str):
            func = getattr(self, function_str)
            func(instructions)
            self.__loger.error('recv instruction %s from client [%s]!' %(instructions, self.client_address))
        else:
            self.__loger.error('%s: %s from client [%s]!' %(self.__code_list, instructions, self.client_address))

    def cd(self, instructions):
        import os
        import json
        print(instructions)
        print(self.__current_path)
        path = json.loads(instructions[1])['path']
        print(os.path.isdir(os.path.abspath(self.__current_path)))
        tmp_path = os.path.abspath(os.path.join(self.__current_path, path))
        print(tmp_path)
        print(os.path.isdir(tmp_path))
        print(self.__check_path(tmp_path))
        if os.path.isdir(tmp_path) and self.__check_path(tmp_path):
            self.__current_path = tmp_path
            response_code = '500'
        else:
            response_code = '501'
        self.request.send(mylib.s2b('{"code":"%s", "path":"%s"}' %(response_code, self.__current_path.replace(self.__home_path, ""))))

    def __check_path(self, path):
        import os
        if path.startswith(os.path.abspath(self.__home_path)):
            return True
        else:
            return False

class myftp():
    def __init__(self):
        self.__server = socketserver.ThreadingTCPServer((conf.SERVER_IP, conf.PORT), Myftphandle)


    def runserver(self):
        print('65ftpserver is running...')
        self.__server.serve_forever()