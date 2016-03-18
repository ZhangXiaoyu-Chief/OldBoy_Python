#!/usr/bin/env python3
# coding:utf-8
import paramiko
import sys
import traceback
from paramiko.py3compat import input
from libs import mylib
from models import interactive, auditlog
from conf import  conf

import os
class myTty(object):
    '''
    myTty类，封装了tty相关属性和方法
    '''
    def __init__(self, user, hostuser):
        self.user = user # 堡垒机用户
        self.hostuser = hostuser # 远端主机用户
        self.username = hostuser.username # 远端主机用户名
        self.ip = hostuser.host.ip_addr # ip地址
        self.port = hostuser.host.port # 端口
        self.password = hostuser.password # 密码



    def get_ssh(self, ip, port, username, password, rsa_key_file = None):
        '''
        获取ssh对象方法
        :param ip: ip地址
        :param port: 端口
        :param username: 用户名
        :param password: 密码
        :param rsa_key_file: keyfile
        :return: ssh对象
        '''
        try:
            client = paramiko.SSHClient() # 创建ssh对象
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 忽略提示是否添加信任列表
            if rsa_key_file and os.path.isfile(rsa_key_file): # 根据不同认证方式连接主机
                client.connect(ip, port,username, password,key_filename = rsa_key_file)
                return client
            else:
                client.connect(ip,port,username, password, timeout = 5)
                return client
        except Exception as e:
            return None

    def run(self):
        '''
        类的入口方法
        :return:
        '''
        print('Connect remote host [%s] as user [%s]...' %(self.ip, self.username))
        client = self.get_ssh(self.ip,  self.port, self.username, self.password) # 获取ssh对象
        if client:
            chan = client.invoke_shell()
            print("Connect success let's go [%s]" %self.user.username)
            auditlog.insert_log(self.user, self.hostuser, u'login', 'login') # 记录登录日志
            interactive.interactive_shell(self.user, self.hostuser, chan, client)
            auditlog.insert_log(self.user, self.hostuser, u'logout', 'logout') # 记录退出日志
            chan.close() # 关闭shell
            client.close() # 关闭ssh通道
            return True
        else:
            mylib.print_err(conf.ERRORNO['5001'])
            return False