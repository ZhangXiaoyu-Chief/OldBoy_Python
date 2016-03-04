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
from conf import conf

class ftpclient(object):
    def __init__(self):
        '''
        初始化客户端方法
        :return: 无
        '''
        self.__current_user = "guest"
        self.__sk = socket.socket()
        self.__conn = self.__sk.connect(conf.IP_PORT)
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
        print(mylib.b2s(self.__sk.recv(100))) # 显示欢迎信息
        while True: # 循环获取用户输入的而命令，如果输入quit退出循环，并退出客户端
            user_input = input('%s >> ' %(self.__current_user)).strip()
            if len(user_input) == 0: continue
            user_input = user_input.split() # 分割用户输入的命令
            if user_input[0] == 'quit': # 判断用户输入的命令，quit表示退出
                break
            if hasattr(self, user_input[0]): # 判断用户命令是否有对应的方法
                func = getattr(self, user_input[0]) # 获取方法
                func(user_input) # 执行方法
            else:
                print(mylib.color('命令输入错误，输入help查看帮助'))


    def get(self, user_input):
        '''
        下载文件方法
        :param user_input: 用户输入命令及参数
        :return: 无
        '''
        import os
        import sys
        if len(user_input) == 2: # 判断用户输入是否符合语法要求
            filename = user_input[1] # 获取要下载的文件名
            tmp_filename = '%s.ftp' %os.path.split(filename)[1] # 定义临时文件名
            if os.path.isfile(tmp_filename): # 判断临时文件是否存在（也就是是否需要续传）
                tmp_file_size = os.path.getsize(tmp_filename) # 获取临时文件的大小
            else:
                tmp_file_size = 0 # 不存在，临时文件大小等于0
            # 通知服务端，文件名，文件已近传输的大小
            self.__sk.sendall(mylib.s2b('get|%s|%s' % (filename, tmp_file_size)))
            # 获取服务端确认消息
            Confirm = mylib.b2s(self.__sk.recv(100))
            count_jindu = 0
            if Confirm.startswith('get|ready'):
                Confirm = Confirm.split('|')
                file_size = int(Confirm[2]) # 从服务端确认消息中获取文件大小
                recv_size = tmp_file_size # 已经传输文件大小等于临时文件大小
                md5 = Confirm[3] # 从确认消息中获取下载文件的md5稍后用于验证
                filename = os.path.split(filename)[1]
                if recv_size == 0: # 通过已接受文件大小确定文件打开方式
                    f = open('%s.ftp' %filename, 'wb')
                else:
                    f = open('%s.ftp' %filename, 'ab')
                # 循环接受文件数据，直到结束
                while file_size != recv_size:
                    data = self.__sk.recv(conf.FILE_PER_SIZE)
                    recv_size += len(data)
                    f.write(data)
                    count = (int(conf.JINDO_MAX * recv_size / file_size) - count_jindu)
                    # sys.stdout.write('#' * int(count))
                    # sys.stdout.flush()
                    mylib.process_bar(recv_size, file_size)
                    count_jindu = int(conf.JINDO_MAX * recv_size / file_size)
                f.close()
                print('')
                print('正在验证下载的文件...')
                # 获取临时文件的md5值
                md5_new = mylib.get_file_md5('%s.ftp' %filename)
                if md5_new == md5: # 校验md5是否一致，一致则重命名文件
                    import shutil
                    shutil.move('%s.ftp' %filename, filename)
                    print('文件验证成功...')
                    print('文件下载成功')
                else:
                    print('文件验证失败...')
            else:
                print(Confirm)
        else:
            print('命令输入错误，输入help查看帮助')


    def put(self, user_input):
        '''
        上传文件方法
        :param user_input: 用户命令
        :return: 无
        '''
        import os
        import sys
        if len(user_input) == 2: # 判断命令是否合法
            filename = user_input[1]
            if os.path.isfile(filename): # 判断要上传的文件是否存在
                file_size = os.path.getsize(filename)
                self.__sk.sendall(mylib.s2b('checkspacesize|%s' %file_size)) # 发送检查剩余空间是否够的命令
                res = mylib.b2s(self.__sk.recv(100)) # 接受消息
                print(res)
                if res == 'can': # 如果空间够则上传
                    md5 = mylib.get_file_md5(filename) # 获取文件md5值
                    self.__sk.sendall(mylib.s2b('put|%s|%s|%s' %(filename, file_size, md5))) # 发送命令告诉服务器要上传的文件、文件大小及md5值
                    res = mylib.b2s(self.__sk.recv(100)) # 获取服务端确认消息
                    #print(res)
                    self.__sk.sendall(mylib.s2b('put|ready')) # 通知服务端准备接收文件
                    if res.startswith('put|ready'):
                        res = res.split('|')
                        send_size = int(res[2]) # 从服务端的而确认消息中获取已经传输的大小，用于续传
                        f = open(filename, 'rb')
                        f.seek(send_size)
                        count_jindu = 0
                        # 循环上传文件数据
                        while file_size != send_size:
                            if file_size - send_size > conf.FILE_PER_SIZE:
                                data = f.read(conf.FILE_PER_SIZE)
                                send_size += conf.FILE_PER_SIZE
                            else:
                                data = f.read(file_size - send_size)
                                send_size += (file_size - send_size)
                            self.__sk.sendall(data)
                            count = (int(conf.JINDO_MAX * send_size / file_size) - count_jindu)
                            sys.stdout.write('#' * int(count))
                            sys.stdout.flush()
                            count_jindu = int(conf.JINDO_MAX * send_size / file_size)
                        msg = mylib.b2s(self.__sk.recv(100)) # 获取服务端返回的上传结果
                        print("")
                        print(msg)
                    else:
                        print(res)
                else:
                    print('空间不足')
        else:
            print('命令输入错误，输入help查看帮助')

    def auth(self, user_input):
        '''
        认证方法
        :param user_input: 用户输入命令
        :return:
        '''
        username = input('username: ') # 获取用户名
        password = input('password: ') # 获取密码
        self.__sk.sendall(mylib.s2b('auth|%s|%s' % (username, mylib.jiami(password)))) # 调用服务端的认证方法，验证用户名密码
        res = mylib.b2s(self.__sk.recv(100)) # 获取验证结果
        print(res)
        if res == 'ok': # 如果验证成功，修改当前用户名和登录状态
            self.__current_user = username
            self.__is_login = True

    def cd(self, user_input):
        '''
        切换目录方法
        :param user_input: 用户命令
        :return:
        '''
        if len(user_input) == 2:
            # 调用服务端切换目录方法，并输出返回结果
            self.__sk.sendall(mylib.s2b('cd|%s' %user_input[1]))
            res = mylib.b2s(self.__sk.recv(100))
            print(res)
        else:
            print('命令输入错误，输入help查看帮助')

    def rm(self, user_input):
        '''
        删除文件方法
        :param user_input: 用户命令
        :return: 无
        '''
        if len(user_input) == 2:
            # 调用服务器端的删除方法，并输出返回的结果
            self.__sk.sendall(mylib.s2b('rm|%s' %user_input[1]))
            res = mylib.b2s(self.__sk.recv(100))
            print(res)
        else:
            print('命令输入错误，输入help查看帮助')

    def move(self, user_input):
        '''
        移动或重名名方法
        :param user_input: 用户命令
        :return: 无
        '''
        if len(user_input) == 3:
            # 调用服务端的相应方法，并输出返回结果
            self.__sk.sendall(mylib.s2b('move|%s|%s' %(user_input[1], user_input[2])))
            res = mylib.b2s(self.__sk.recv(100))
            print(res)
        else:
            print('命令输入错误，输入help查看帮助')


    def pwd(self, user_input):
        '''
        显示当前目录方法
        :param user_input:
        :return:
        '''
        if len(user_input) == 1:
            self.__sk.sendall(mylib.s2b('pwd'))
            res = mylib.b2s(self.__sk.recv(100))
            print(res)
        else:
            print('命令输入错误，输入help查看帮助')

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
        '''
        查看目录内容方法
        :param user_input: 用户命令
        :return: 无
        '''
        if len(user_input) == 1:
            self.__runcmd(user_input[0])

    def __runcmd(self, cmd):
        '''
        执行原生shell命令方法
        :param cmd: shell命令
        :return: 无
        '''
        self.__sk.sendall(mylib.s2b(cmd))
        server_ack_msg = self.__sk.recv(100)
        cmd_res_msg = str(server_ack_msg.decode()).split("|")
        print(cmd_res_msg)
        if cmd_res_msg[0] == "CMD_RESULT_SIZE":
            cmd_res_size = int(cmd_res_msg[1])
            self.__sk.send(b"CLIENT_READY_TO_RECV")
        res = ''
        received_size = 0
        while received_size < cmd_res_size:
            data = self.__sk.recv(500)
            received_size += len(data)
            res += str(data.decode())
        else:
            print(str(res))
