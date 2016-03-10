#!/usr/bin/env python3
# coding:utf-8
import socketserver
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
        self.__current_user = "guest" # 定义默认用户，默认用户为guest
        self.__current_path = '' # 定义当前目录，默认是空，也即是家目录
        self.__code_list = conf.CODE_LIST # 定义错误码列表
        self.__sk = socket.socket() # 定义socket对象
        self.__conn = self.__sk.connect((conf.SERVER_IP, conf.PORT))
        self.__is_login = False # 保存登录状态
        self.__tmp_path = conf.TMP_PATH
        self.__help_info = {
            "get" : "用于下载文件，格式：get path/to/filename [dst/path/to/]，说明：path/to/格式要求同cd命令, dst/path/to/为目标目录，暂时只能使用相对目录",
            "put" : "用于上传文件，格式：put path/to/filename，说明：path/to/格式要求同cd命令",
            "auth" : "用户认证，格式：auth，然后根据提示输入用户名及密码",
            "ls" : "用于显示当前目录下文件或文件详细信息，格式：ls",
            "cd" : "用于切换服务端目录，格式：cd path/to/，说明只能使用相对目录，‘.’表示当前目录，‘..’表示父目录",
            "rm" : "用于删除文件或目录，格式：rm path/to[/filename]，说明：path/to/格式要求同cd命令",
        } # 帮助信息
        self.__version_info = '''
--------------------------------------------------------------------------------------------
欢迎使用65ftp
version 2.0
版本记录：
1、优化了代码
2、修改了rm、cd命令的目录算法，尤其是修改了目录是否合法的算法，使命令更符合原生linux使用习惯
3、修改了家目录已使用大小的算法，使用原生du -s获取已经使用的大小
4、修复了上传的bug
5、服务端和客户端分离，成为两个独立的目录，并使用不通的配置文件
6、使用错误码列表的方式统一了报错信息
7、服务端增加日志输出
8、取消了pwd命令，当前目录直接显示在命令提示符上
9、get命令增加了可以保存到其他目录的功能
--------------------------------------------------------------------------------------------
        ''' # 版本信息

    def start(self):
        '''
        启动客户端方法
        :return: 无
        '''
        print('欢迎使用65ftp，version: 2.0\n 输入help查看帮助信息')
        while True: # 循环获取用户输入的而命令，如果输入quit退出循环，并退出客户端
            user_input = input(r'%s:%s>> ' %(self.__current_user, self.__current_path)).strip()
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
        '''
        客户端下载方法
        :param user_input: 用户输入的指令
        :return: 无
        '''
        import os
        if len(user_input) == 2: # 如果是get xxx，则表示下载到当前目录
            dst_path = '.'
        elif len(user_input) == 3: # 如果是 get xxx xxx，则表示要下载到其他目录
            dst_path = user_input[2]
        else:
            print(self.__code_list['401'])
            return None
        if os.path.isdir(dst_path): # 判断目标文件是否存在
            filename = user_input[1] # 获取下载的文件名
            tmp_filename = os.path.join(self.__tmp_path,'%s.ftp' %os.path.split(filename)[1]) # 定义临时文件
            if os.path.isfile(tmp_filename): # 判断临时文件是否存在（也就是是否需要续传）
                tmp_file_size = os.path.getsize(tmp_filename) # 获取临时文件的大小
            else:
                tmp_file_size = 0
            self.__sk.send(mylib.s2b(r'get|{"filename":"%s", "sendsize": %s}' %(filename, tmp_file_size))) # 向服务端发送下载指令接文件名和已近下载的大小
            Confirm = mylib.b2s(self.__sk.recv(100)).split('|') # 获取服务器反馈
            if Confirm[0] == 'ready': # 如果是ready则准备下载文件
                file_size = json.loads(Confirm[1])['filesize'] # 获取文件大小
                md5 = json.loads(Confirm[1])['md5'] # 获取md5
                recv_size = tmp_file_size
                f = open(tmp_filename, 'ab')
                while file_size != recv_size:
                    # 只要已下载大小不等于文件大小则循环接受数据
                    try:
                        data = self.__sk.recv(conf.FILE_PER_SIZE)
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
                print('')
                print('Validating...')
                new_md5 = mylib.get_file_md5(tmp_filename)
                if new_md5 == md5: # 验证md5，如果验证通过修改成正式文件名，如果没验证过去删除临时文件
                    import shutil
                    shutil.move(tmp_filename, os.path.join(dst_path, filename))
                else:
                    os.remove(tmp_filename)
            else:
                print(self.__code_list[Confirm[1]])
        else:
            print(self.__code_list['304'])


    def put(self, user_input):
        '''
        客户端上传方法
        :param user_input: 指令
        :return: 无
        '''
        import json
        if len(user_input) == 2:
            file_name = user_input[1]
            if not os.path.isfile(file_name):
                print(self.__code_list['302'])
                return None
            self.__sk.sendall(mylib.s2b('checkspacesize'))
            res = json.loads(mylib.b2s(self.__sk.recv(100)))
            free_size = int(res['freesize']) * 1024 * 1024 # 获取剩余空间大小
            file_size = os.path.getsize(file_name)
            if free_size > file_size: # 判断剩余空间是否够，够就下载，不够就直接返回
                md5 = mylib.get_file_md5(file_name) # 获取上传文件的md5
                self.__sk.send(mylib.s2b(r'put|{"filename":"%s", "file_size":%s, "md5":"%s"}' %(os.path.split(file_name)[1], file_size, md5))) # 发送上传指令，并通知服务端文件名，文件大小和md5
                res = mylib.b2s(self.__sk.recv(200)).split('|') # 获取服务端确认信息
                if res[0] == 'ready':
                    send_size = json.loads(res[1])['recv_size'] # 获取已经上传的大小
                    f = open(file_name, 'rb')
                    f.seek(send_size) # 设定文件的其实位置为已上传的大小
                    while file_size != send_size:
                        # 只要文件大小不等于上传的大小则循环读文件并上传数据
                        if file_size - send_size > conf.FILE_PER_SIZE:
                            data = f.read(conf.FILE_PER_SIZE)
                            send_size += conf.FILE_PER_SIZE
                        else:
                            data = f.read(file_size - send_size)
                            send_size += (file_size - send_size)
                        self.__sk.send(data)
                        mylib.process_bar(send_size, file_size)
                    print(mylib.b2s(self.__sk.recv(200)))
                    print("")
            else:
                print(self.__code_list['307'])
        else:
            print(self.__code_list['401'])

    def auth(self, user_input):
        '''
        认证方法
        :param user_input: 用户输入命令
        :return:
        '''
        if len(user_input) ==1:
            username = input('username: ') # 获取用户名
            password = input('password: ') # 获取密码
            self.__sk.sendall(mylib.s2b(r'auth|{"username":"%s", "password":"%s"}' % (username, mylib.jiami(password)))) # 调用服务端的认证方法，验证用户名密码
            res = mylib.b2s(self.__sk.recv(200)) # 获取验证结果
            print(self.__code_list[res])
            if res == '200': # 如果验证成功，修改当前用户名和登录状态
                self.__current_user = username
                self.__is_login = True
        else:
            print(self.__code_list['401'])

    def cd(self, user_input):
        '''
        切换服务端目录方法
        :param user_input: 用户指令
        :return: 无
        '''
        if len(user_input) == 2:
            self.__sk.send(mylib.s2b('cd|{"path" : "%s"}' %user_input[1])) # 发送cd指令
            res = json.loads(mylib.b2s(self.__sk.recv(200))) # 获取服务端反馈
            if res['code'] == '500':
                self.__current_path = res['path'] # 修改当前目录等于返回来的目录
            else:
                print(self.__code_list[res['code']])
        else:
            print(self.__code_list['401'])

    def ls(self, user_input):
        '''
        查看目录内容方法
        :param user_input: 用户命令
        :return: 无
        '''
        if len(user_input) == 1:
            self.__runcmd(user_input[0]) # 调用self.__runcmd执行原生linux命令
        else:
            print(self.__code_list['401'])

    def __runcmd(self, cmd):
        '''
        执行原生shell命令方法
        :param cmd: shell命令
        :return: 无
        '''
        self.__sk.sendall(mylib.s2b(cmd))
        server_ack_msg = self.__sk.recv(100)
        cmd_res_msg = str(server_ack_msg.decode()).split("|")
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

    def help(self, user_input):
        '''
        显示帮助方法
        :param user_input: 用户命令
        :return: 无
        '''
        if len(user_input) == 1:
            print(self.__version_info)
            for key,item in self.__help_info.items():
                print("%s:  %s" %(key.rjust(8), item))
        elif len(user_input) == 2 and self.__help_info.get(user_input[1]):
            print("%s:  %s" %(user_input[1].rjust(8), self.__help_info.get(user_input[1])))
        else:
            print(self.__code_list['401'])

    def rm(self, user_input):
        '''
        删除文件方法
        :param user_input: 用户命令
        :return: 无
        '''
        if len(user_input) == 2:
            self.__sk.send(mylib.s2b('rm|{"path" : "%s"}' %user_input[1])) # 向服务端发送删除指令
            res = json.loads(mylib.b2s(self.__sk.recv(200))) # 获取执行结果（错误码）
            print(self.__code_list[res['code']])
        else:
            print(self.__code_list['401'])

    def exit(self, user_input):
        self.__sk.close()
        exit(0)