#!/usr/bin/env python3
# coding:utf-8
import socketserver
from libs import mylib
import subprocess
from conf import conf
from model.users import users,user
from libs import mylib


import os,sys
import socket
import json


class ftpclient(object):
    def __init__(self):
        '''
        初始化客户端方法
        :return: 无
        '''
        self.__current_user = "guest"
        self.__current_path = ''
        self.__code_list = conf.CODE_LIST
        self.__sk = socket.socket()
        self.__conn = self.__sk.connect((conf.SERVER_IP, conf.PORT))
        self.__is_login = False # 保存登录状态
        self.__help_info = {
            "get" : "用于下载文件，格式：get path/to/filename，说明：path/to/格式要求同cd命令",
            "put" : "用于上传文件，格式：put path/to/filename，说明：path/to/格式要求同cd命令",
            "auth" : "用户认证，格式：auth，然后根据提示输入用户名及密码",
            "pwd" : "用于显示当前目录，格式：pwd",
            "ls" : "用于显示当前目录下文件或文件详细信息，格式：ls",
            "cd" : "用于切换服务端目录，格式：cd path/to/，说明~或/表示用户家目录，但是不能/path/to/或 ~/path/to/，‘.’表示当前目录，‘..’表示父目录",
            "rm" : "用于删除文件或目录，格式：rm path/to[/filename]，说明：path/to/格式要求同cd命令",
            "move" : "用于移动或重命名文件，格式：move path/to[/old_filename] move path/to[/new_filename]，说明：path/to/格式要求同cd命令"
        }

    def start(self):
        '''
        启动客户端方法
        :return: 无
        '''

        while True: # 循环获取用户输入的而命令，如果输入quit退出循环，并退出客户端
            user_input = input('%s:/%s>> ' %(self.__current_user, self.__current_path)).strip()
            if len(user_input) == 0: continue
            user_input = user_input.split() # 分割用户输入的命令
            if user_input[0] == 'quit': # 判断用户输入的命令，quit表示退出
                break
            if hasattr(self, user_input[0]): # 判断用户命令是否有对应的方法
                func = getattr(self, user_input[0]) # 获取方法
                func(user_input) # 执行方法
            else:
                print(self.__code_list['401'])


    def get(self, user_input):
        pass


    def put(self, user_input):
        pass

    def auth(self, user_input):
        '''
        认证方法
        :param user_input: 用户输入命令
        :return:
        '''
        username = input('username: ') # 获取用户名
        password = input('password: ') # 获取密码
        self.__sk.sendall(mylib.s2b('auth|%s|%s' % (username, mylib.jiami(password)))) # 调用服务端的认证方法，验证用户名密码
        res = mylib.b2s(self.__sk.recv(200)) # 获取验证结果
        print(res)
        if res == 'ok': # 如果验证成功，修改当前用户名和登录状态
            self.__current_user = username
            self.__is_login = True

    def cd(self, user_input):
        if len(user_input) == 2:
            self.__sk.send(mylib.s2b('cd|{"path" : "%s"}' %user_input[1]))
            res = json.loads(mylib.b2s(self.__sk.recv(200)))
            print(res)
            print(type(res))
            if res['code'] == '500':
                self.__current_path = res['path']
            else:
                print(self.__code_list[code])
        else:
            print(self.__code_list['401'])


    def rm(self, user_input):
        pass

    def move(self, user_input):
        pass


    def pwd(self, user_input):
        pass

    def help(self, user_input):
        '''
        显示帮助方法
        :param user_input: 用户命令
        :return:
        '''
        if len(user_input) == 1:
            for key,item in self.__help_info.items():
                print("%s:  %s" %(key.rjust(8), item))
        elif len(user_input) == 2 and self.__help_info.get(user_input[1]):
            print("%s:  %s" %(user_input[1].rjust(8), self.__help_info.get(user_input[1])))
        else:
            print('命令输入错误或要查询的命令不存在')

    def ls(self, user_input):
        pass

    def __runcmd(self, cmd):
        pass