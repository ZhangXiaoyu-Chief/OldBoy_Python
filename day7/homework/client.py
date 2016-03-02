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
        self.__current_user = None
        self.__sk = socket.socket()
        self.__conn = self.__sk.connect(conf.IP_PORT)
        self.__is_login = False

    def start(self):
        print(mylib.b2s(self.__sk.recv(100)))
        while True:

            user_input = input('>> ').strip()
            if len(user_input) == 0: continue
            user_input = user_input.split()
            if user_input[0] == 'quit':
                break
            if hasattr(self, user_input[0]):
                func = getattr(self, user_input[0])
                func(user_input)

            else:
                print(mylib.color('命令输入错误，输入help查看帮助'))


    def get(self, user_input):
        import os
        import sys
        print(user_input)
        if len(user_input) == 2:
            filename = user_input[1]
            tmp_filename = '%s.ftp' %filename
            if os.path.isfile(tmp_filename):
                tmp_file_size = os.path.getsize(tmp_filename)
            else:
                tmp_file_size = 0
            self.__sk.sendall(mylib.s2b('get|%s|%s' % (filename, tmp_file_size)))
            Confirm = mylib.b2s(self.__sk.recv(100))
            count_jindu = 0
            max_count_jindu = 20
            if Confirm.startswith('get|ready'):
                Confirm = Confirm.split('|')
                print(Confirm)
                file_size = int(Confirm[2])
                recv_size = tmp_file_size
                md5 = Confirm[3]
                filename = os.path.split(filename)[1]
                if recv_size == 0:
                    f = open('%s.ftp' %filename, 'wb')
                else:
                    f = open('%s.ftp' %filename, 'ab')
                while file_size != recv_size:
                    data = self.__sk.recv(conf.FILE_PER_SIZE)
                    recv_size += len(data)
                    f.write(data)
                    #print(recv_size, file_size)
                    #print(recv_size/file_size)
                    count = (int(conf.JINDO_MAX*recv_size/file_size) - count_jindu)
                    #
                    #print(int(20*recv_size/file_size))
                    sys.stdout.write('#' * int(count))
                    sys.stdout.flush()
                    #print('\n')
                    count_jindu = int(conf.JINDO_MAX*recv_size/file_size)
                    #print(count_jindu)
                    #print(file_size, recv_size)
                #print('\n---get file ok-----')

                f.close()
                md5_new = mylib.get_file_md5('%s.ftp' %filename)
                print('')
                if md5_new == md5:
                    import shutil
                    shutil.move('%s.ftp' %filename, filename)
                print('---get file ok-----')

            else:
                print(Confirm)
        else:
            print('命令输入错误，输入help查看帮助')


    def put(self, user_input):
        import os
        if len(user_input) == 2:
            filename = user_input[1]
            if os.path.isfile(filename):

                file_size = os.path.getsize(filename)
                self.__sk.sendall(mylib.s2b('checkspacesize|%s' %file_size))
                res = mylib.b2s(self.__sk.recv(100))
                print(res)
                if res == 'can':
                    md5 = mylib.get_file_md5(filename)
                    self.__sk.sendall(mylib.s2b('put|%s|%s|%s' %(filename, file_size, md5)))
                    res = mylib.b2s(self.__sk.recv(100))
                    print(res)
                    self.__sk.sendall(mylib.s2b('put|ready'))
                    if res.startswith('put|ready'):
                        res = res.split('|')
                        send_size = int(res[2])
                        f = open(filename, 'rb')
                        f.seek(send_size)
                        while file_size != send_size:
                            if file_size - send_size > conf.FILE_PER_SIZE:
                                data = f.read(conf.FILE_PER_SIZE)
                                send_size += conf.FILE_PER_SIZE
                            else:
                                data = f.read(file_size - send_size)
                                send_size += (file_size - send_size)
                            self.__sk.sendall(data)
                    else:
                        print(res)
                else:
                    print('空间不足')
        else:
            print('命令输入错误，输入help查看帮助')


                    #print(file_size, send_size)

        # filename = self.__current_path + client_cmd[1]
        #
        # if os.path.isfile(filename):
        #     file_size = os.path.getsize(filename)
        #     res = "get|ready|%s" %file_size
        #     self.request.sendall(mylib.s2b(res))
        #     f = open(filename, 'rb')
        #     send_size = int(client_cmd[2])
        #     f.seek(send_size)
        #     while file_size != send_size:
        #         if file_size - send_size > 1024:
        #             data = f.read(1024)
        #             send_size += 1024
        #         else:
        #             data = f.read(file_size - send_size)
        #             send_size += (file_size - send_size)
        #         self.request.sendall(data)
        #         print(file_size, send_size)
    def auth(self, user_input):
        print(user_input)
        usename = input('username: ')
        password = input('password: ')
        self.__sk.sendall(mylib.s2b('auth|%s|%s' % (usename, mylib.jiami(password))))
        res = mylib.b2s(self.__sk.recv(100))

        print(res)
        if res == 'ok':
            self.__is_login = True
        print(self.__is_login)

    def cd(self, user_input):
        if len(user_input) != 2:
            print(user_input)
            self.__sk.sendall(mylib.s2b('cd|%s' %user_input[1]))
            res = mylib.b2s(self.__sk.recv(100))
            print(res)
        else:
            print('命令输入错误，输入help查看帮助')

    def rm(self, user_input):

        print(user_input)
        if len(user_input) == 2:
            print(user_input)
            self.__sk.sendall(mylib.s2b('rm|%s' %user_input[1]))
            res = mylib.b2s(self.__sk.recv(100))
            print(res)
        else:
            print('命令输入错误，输入help查看帮助')

    def move(self, user_input):
        if len(user_input) == 3:
            print(user_input)
            self.__sk.sendall(mylib.s2b('move|%s|%s' %(user_input[1], user_input[2])))
            res = mylib.b2s(self.__sk.recv(100))
            print(res)
        else:
            print('命令输入错误，输入help查看帮助')


    def pwd(self, user_input):
        if len(user_input) == 1:
            self.__sk.sendall(mylib.s2b('pwd'))
            res = mylib.b2s(self.__sk.recv(100))
            print(res)
        else:
            print('命令输入错误，输入help查看帮助')

if __name__ == "__main__":
    f = ftpclient()
    f.start()
