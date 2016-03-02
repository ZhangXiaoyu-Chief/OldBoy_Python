#!/usr/bin/env python
# coding:utf-8
import socketserver
from libs import mylib
import subprocess
from conf import conf
from model import users
class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        #print(self)
        # 定义当前用户，用来保存当前用户信息
        self.__current_user = {
        "username" : "guest",
        "home" : "home/tmp/",
        "max_size" : conf.TMP_SPACE_SIZE
        }
        # 定义用户对象
        self.__userobj = users.users()

        # self.__users = self.__userobj.get_users()
        # print(self.__users)
        conn = self.request
        # 用户连接后后显示的信息
        conn.sendall(bytes('欢迎使用65ftp','utf8'))
        # 获取当前目录
        self.__current_path = self.__current_user['home']

        flag = True
        while flag:
            pass
            # 获取用户命令
            client_cmd = mylib.b2s(conn.recv(100))
            # 将用户命令进行分割，客户端传过来的命令需要使用|分割命令本身和命令相关参数
            client_cmd = client_cmd.split("|")
            # 获取命令
            if client_cmd[0] == 'quit': # 如果是quit，退出当前循环，释放连接
                flag = False
                continue
            if hasattr(self, client_cmd[0]): # 根据命令执行相应的方法
                func = getattr(self, client_cmd[0])
                func(client_cmd)
        conn.close()

    def get(self, client_cmd):
        '''
        下载文件方法
        :param client_cmd: 分割后的命令
        :return: 无
        '''
        print(client_cmd)
        import os
        # 拼接
        filename = self.__current_path + client_cmd[1]

        if os.path.isfile(filename):
            md5 = mylib.get_file_md5(filename)
            file_size = os.path.getsize(filename)
            res = "get|ready|%s|%s" %(file_size, md5)
            self.request.sendall(mylib.s2b(res))
            f = open(filename, 'rb')
            send_size = int(client_cmd[2])
            f.seek(send_size)
            while file_size != send_size:
                if file_size - send_size > conf.FILE_PER_SIZE:
                    data = f.read(conf.FILE_PER_SIZE)
                    send_size += conf.FILE_PER_SIZE
                else:
                    data = f.read(file_size - send_size)
                    send_size += (file_size - send_size)
                self.request.sendall(data)
                print(file_size, send_size)
        else:
            res = "文件%s不存在" %filename
            self.request.sendall(mylib.s2b(res))

    def put(self, client_cmd):
        import os
        filename = self.__current_path + os.path.split(client_cmd[1])[1]
        file_size = int(client_cmd[2])
        #filename = os.path.split(filename)[1]
        md5 = client_cmd[3]
        tmp_filename = '%s.ftp' %filename

        print(client_cmd)
        if os.path.isfile(tmp_filename):
            tmp_file_size = os.path.getsize(tmp_filename)
        else:
            tmp_file_size = 0
        self.request.sendall(mylib.s2b('put|ready|%s' %tmp_file_size))
        Confirm = mylib.b2s(self.request.recv(100))
        recv_size = tmp_file_size
        if Confirm.startswith('put|ready'):
            Confirm = Confirm.split('|')

            if recv_size == 0:
                f = open('%s.ftp' %filename, 'wb')
            else:
                f = open('%s.ftp' %filename, 'ab')
            while file_size != recv_size:
                #print(data)
                data = self.request.recv(conf.FILE_PER_SIZE)
                #print(data)
                recv_size += len(data)
                print(type(file_size))
                print(recv_size, file_size)
                f.write(data)
            #print('\n---put file ok-----')



            f.close()
            new_md5 = mylib.get_file_md5('%s.ftp' %filename)
            print(md5, new_md5)
            import shutil
            if md5 == new_md5:
                shutil.move('%s.ftp' %filename, filename)
            #print('ready')
        #else:
            #print(Confirm)

            #print('---getfile----')

    def checkspacesize(self, client_cmd):
        file_size = client_cmd[1]
        free_size = self.__current_user['max_size'] - mylib.get_dir_size_for_linux(self.__current_path)
        if file_size < free_size:
            self.request.sendall(mylib.s2b('can'))
        else:
            self.request.sendall(mylib.s2b('not'))


    def auth(self, client_cmd):
        print(client_cmd)
        user = self.__userobj.get_user(client_cmd[1])
        print(user)
        if user:
            if user['password'] == client_cmd[2]:
                self.__current_user = user
                self.__current_path = user['home']
                self.request.sendall(mylib.s2b('ok'))
            else:
                self.request.sendall(mylib.s2b('fail'))
        else:
            self.request.sendall(mylib.s2b('fail'))

    def cd(self, client_cmd):
        print(client_cmd)
        path = client_cmd[1]
        import os
        if path == '.':
            pass
        elif path == '..':
            if self.__current_path == self.__current_user['home']:
                self.request.sendall(mylib.s2b('ok'))
            else:
                #self.__current_path = os.path.split(self.__current_path)[0] + '/'
                self.__current_path = os.path.split(self.__current_path[0:len(self.__current_path)-1])[0] + '/'
                print(os.path.split(self.__current_path[0:len(self.__current_path)-1]))

                self.request.sendall(mylib.s2b('ok'))
        elif path == '/' or path == '~':
            self.__current_path = self.__current_user['home']
        else:
            if os.path.isdir(self.__current_path + path):
                self.__current_path += path + '/'
                self.request.sendall(mylib.s2b('ok'))
            else:
                self.request.sendall(mylib.s2b('目录%s不存在' %path))

    def rm(self, cliend_cmd):
        filename = self.__current_path + cliend_cmd[1]
        print(filename)
        print(cliend_cmd)
        import os
        import shutil
        if os.path.isdir(filename):
            shutil.rmtree(filename)
            self.request.sendall(mylib.s2b('ok'))
        elif os.path.isfile(filename):
            os.remove(filename)
            self.request.sendall(mylib.s2b('ok'))
        else:
            self.request.sendall(mylib.s2b('目录或文件%s不存在' %filename))


    def ls(self, cliend_cmd):
        pass

    def move(self, cliend_cmd):
        import shutil
        import os
        filename = self.__current_path + cliend_cmd[1]
        new_filename = self.__current_path + cliend_cmd[2]
        if os.path.isfile(filename) or os.path.isdir(filename):
            print(filename, new_filename)
            shutil.move(filename, new_filename)
            self.request.sendall(mylib.s2b('ok'))
        else:
            self.request.sendall(mylib.s2b('目录或文件%s不存在' %filename))

    def pwd(self, client_cmd):
        print(self.__current_path)
        self.request.sendall(mylib.s2b(self.__current_path))

    def runcmd(self):
        flag = True
        while True:
            pass

class myftp():
    def __init__(self):
        self.__server = socketserver.ThreadingTCPServer(('127.0.0.1', 9999), Myserver)
    def runserver(self):
        self.__server.serve_forever()