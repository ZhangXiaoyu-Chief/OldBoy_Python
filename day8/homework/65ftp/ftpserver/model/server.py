#!/usr/bin/env python3
# coding:utf-8
import socketserver
from conf import conf
from model.users import users,user
from libs import mylib
import socket


class Myftphandle(socketserver.BaseRequestHandler):
    def handle(self):
        '''
        handle方法
        :return: 无
        '''
        import os
        self.__loger = mylib.mylog(conf.LOGS, isstream = True) # 定义日志对象
        self.__current_user = user('guest', '', conf.DEFAULT_QUOTA) # 定义默认用户
        self.__users = users() # 获取users对象
        self.__home_path =  os.path.abspath(os.path.join(conf.HOME_PATH,self.__current_user.get_username())).replace('\\', '/') # 获取家目录
        self.__current_path = self.__home_path # 定义当前目录
        self.__code_list = conf.CODE_LIST # 定义错误里诶表
        self.__loger.info('Client %s:%s is connect the server' %self.client_address)
        while  True:
            try:
                data = mylib.b2s(self.request.recv(1024)) # 获取客户端命令
            except socket.error as e:
                self.__loger.info('Has lost client %s:%s' %self.client_address)
                break
            if not data:
                self.__loger.info('Has lost client %s:%s' %self.client_address)
                break     #如果收不到客户端数据了（代表客户端断开了），就断开
            self.instruction_allowcation(data) #客户端发过来的数据统一交给功能分发器处理

    def instruction_allowcation(self, instructions):
        '''
        命令分发方法
        :param instructions:
        :return:
        '''
        instructions = instructions.split("|")
        function_str = instructions[0] # 客户端发过来的指令中,第一个参加都必须在服务器端有相应的方法处理
        if hasattr(self, function_str):
            func = getattr(self, function_str)
            self.__loger.info('recv instruction %s from client [%s]!' %(instructions, self.client_address))
            func(instructions)
        else:
            self.__loger.error('%s: %s from client [%s]!' %(self.__code_list, instructions, self.client_address))

    def cd(self, instructions):
        '''
        cd命令方法
        :param instructions: 客户端命令
        :return: 无
        '''
        import os
        import json
        path = json.loads(instructions[1])['path'] # 获取要cd的目录
        tmp_path = os.path.abspath(os.path.join(self.__current_path, path)) # 定义临时目录
        if os.path.isdir(tmp_path) and self.__check_path(tmp_path): #判断目录是否存在和是否绕过家目录
            self.__current_path = tmp_path.replace('\\', '/')
            response_code = '500'
        else:
            response_code = '303'
        self.request.send(mylib.s2b('{"code":"%s", "path":"%s"}' %(response_code, self.__current_path.replace(self.__home_path, "")))) # 返回当前目录

    def get(self, instructions):
        '''
        get 指令方法
        :param instructions: 客户端命令
        :return: 无
        '''
        import os
        import json
        res = json.loads(instructions[1])
        filename = os.path.join(self.__current_path, res['filename']) # 获取文件名
        if os.path.isfile(filename) and self.__check_path(filename): # 判断文件是否存在以及是否在家目录范围内
            md5 = mylib.get_file_md5(filename) # 获取下载文件的md5
            file_size = os.path.getsize(filename) # 获取下载文件的大小
            self.request.send(mylib.s2b('ready|{"filesize":%s, "md5": "%s"}' %(file_size, md5))) # 通知客户端准备下载和MD5
            f = open(filename, 'rb')
            send_size = res['sendsize'] # 获取已经下载的大小
            f.seek(send_size) # 设定起始位置，用于续传
            self.__loger.info('Begin send file  %s to client [%s]' %(filename, self.client_address))
            while file_size != send_size:
                # 传输读取文件内容并传输，如果剩余大小每次传输的大小，则传输固定大小，如果剩余的大小
                if file_size - send_size > conf.FILE_PER_SIZE:
                    data = f.read(conf.FILE_PER_SIZE)
                    send_size += conf.FILE_PER_SIZE
                else:
                    data = f.read(file_size - send_size)
                    send_size += (file_size - send_size)
                try:
                    self.request.send(data)
                except socket.error as e:
                    self.__loger.error('%s when send file %s to client [%s]' %(e, filename, self.client_address))
                    break
                print(file_size, send_size)
            f.close()
            self.__loger.info('End send file %s to client [%s]' %(filename, self.client_address))
        else:
            self.request.send(mylib.s2b('fail|303'))

    def auth(self, instructions):
        '''
        用户认证方法，默认用户为guest用户，认证成功后切换用户
        :param instructions: 客户端指令
        :return: 无
        '''
        import json
        import os
        res = json.loads(instructions[1])
        user = self.__users.get_user(res['username']) # 通过用户名获取用户信息

        # 判断用户是否存在
        if user:
            # 判断密码是否正确
            print(user.get_password())
            if user.get_password() == res['password']:
                # 如果验证当前用户等于认证成功的用户
                self.__current_user = user
                # 当前目录等于用户的家目录
                self.__current_path = os.path.abspath(os.path.join(conf.HOME_PATH,self.__current_user.get_username())).replace('\\', '/')
                # 告诉客户端用户成功
                self.request.sendall(mylib.s2b('200'))
                self.__loger.info('%s from [%s]' %(self.__code_list['200'], self.client_address))
            else:
                self.request.sendall(mylib.s2b('201'))
                self.__loger.error('%s from [%s]' %(self.__code_list['201'], self.client_address))
        else:
            self.request.sendall(mylib.s2b('201'))
            self.__loger.error('%s from [%s]' %(self.__code_list['201'], self.client_address))

    def put(self, instructions):
        '''
        put方法
        :param instructions: 客户端指令
        :return: 无
        '''
        import os
        import json

        res = json.loads(instructions[1])
        file_name = os.path.join(self.__current_path, res['filename']) # 获取上传的文件名
        md5 = res['md5'] # 获取上传的文件的md5
        tmp_file_name = os.path.join(self.__current_path, '%s.ftp' %res['filename']) # 定义临时文件
        if os.path.isfile(tmp_file_name): # 判断临时文件，如果存在说明没传完，将续传
            tmp_file_size = os.path.getsize(tmp_file_name) # 获取已经上传的大小
        else:
            tmp_file_size = 0
        self.request.send(mylib.s2b(r'ready|{"recv_size":%s}' %tmp_file_size)) # 通知客户端准备上传并返回已近上传的大小
        recv_size = tmp_file_size
        file_size = res['file_size']
        f = open(tmp_file_name, 'ab')
        self.__loger.info('Begin recv file  %s from client [%s]' %(file_name, self.client_address))
        while recv_size != file_size:
            # 只要已上传的大小不等于文件的大小就循环获取数据写入文件
            try:
                data = self.request.recv(conf.FILE_PER_SIZE)
                recv_size += len(data)
                f.write(data)
                mylib.process_bar(recv_size, file_size)
            except socket.error as e:
                print(self.__code_list['306'])
                f.close()
                break
            except IOError as e:
                print(self.__code_list['305'])
                f.close()
                break
        f.close()
        self.__loger.info('End recv file  %s from client [%s]' %(file_name, self.client_address))
        new_md5 = mylib.get_file_md5(tmp_file_name) # 获取上传后的md5值
        self.__loger.info('Begin validate md5 [%s]' %tmp_file_name)
        if new_md5 == md5: # 验证md5，成功则将临时文件名改为正式文件名
            import shutil
            shutil.move(tmp_file_name, file_name)
            self.request.sendall(mylib.s2b('308'))
            self.__loger.info('%s %s' %(self.__code_list['308'], tmp_file_name))
        else:
            os.remove(tmp_file_name)
            self.request.sendall(mylib.s2b('309'))
            self.__loger.info('%s %s' %(self.__code_list['309'], tmp_file_name))
        self.__loger.info('End validate md5 [%s]' %tmp_file_name)

    def rm(self, instructions):
        '''
        删除文件方法
        :param cliend_cmd: 用户命令
        :return: 无
        '''
        import json
        import os
        import shutil
        res = json.loads(instructions[1])
        filename = os.path.join(self.__current_path, res['path'])
        if self.__check_path(filename):
            if os.path.isdir(filename):# 如果是目录递归删除目录
                shutil.rmtree(filename)
                response_code = '500'
            elif os.path.isfile(filename): # 如果是文件，只删除文件
                os.remove(filename)
                response_code = '500'
            self.__loger.info('%s to rm %s' %(self.__code_list['500'], filename))
        else:
            # 其他情况说明文件或目录不存在
            #self.request.sendall(mylib.s2b('310'))
            response_code = '310'
            self.__loger.info('%s to rm %s' %(self.__code_list['310'], filename))
        self.request.send(mylib.s2b('{"code":"%s"}' %response_code)) # 返回错误码




    def checkspacesize(self, instructions):
        '''
        检查剩余空间是否可以上传文件方法
        :param client_cmd: 用户命令
        :return: 无
        '''
        # 获取剩余空间大小
        import subprocess
        cmd_call = subprocess.Popen('du -s %s' %self.__home_path, shell = True, stdout = subprocess.PIPE)
        res = cmd_call.stdout.read()

        # 计算剩余空间，并返回
        free_size = self.__current_user.get_quota() * 1024 * 1024 - int(mylib.b2s(res).split()[0])
        self.request.send(mylib.s2b(r'{"freesize":%s}' %free_size))

    def __check_path(self, path):
        '''
        检查目录是否超出家目录范围，只要目录不是以家目录开头统统认为是超出家目录范围
        :param path: 要判断的文件或者目录
        :return:
        '''
        import os
        if path.startswith(os.path.abspath(self.__home_path)):
            return True
        else:
            return False

    def ls(self, client_cmd):
        '''
        查看目录内容方法
        :param client_cmd: 用户命令
        :return:
        '''
        self.__runcmd("%s -al %s" %(client_cmd[0], self.__current_path))

    def __runcmd(self, cmd):
        '''
        执行原生shell命令方法
        :param cmd: 命令
        :return:
        '''
        import subprocess
        cmd_call = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cmd_result = cmd_call.stdout.read() # 获取命令执行结果
        ack_msg = mylib.s2b("CMD_RESULT_SIZE|%s" %len(cmd_result))
        self.request.send(ack_msg) # 返回命令执行结果的大小
        client_ack = self.request.recv(50)
        if client_ack.decode() == 'CLIENT_READY_TO_RECV':
            self.request.send(cmd_result) # 返回执行结果

class myftp():
    def __init__(self):
        self.__server = socketserver.ThreadingTCPServer((conf.SERVER_IP, conf.PORT), Myftphandle)

    def runserver(self):
        print('65ftpserver is running...')
        self.__server.serve_forever()