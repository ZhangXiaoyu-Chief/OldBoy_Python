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
        self.__users = users()
        self.__home_path =  os.path.abspath(os.path.join(conf.HOME_PATH,self.__current_user.get_username())).replace('\\', '/')
        self.__current_path = self.__home_path
        self.__code_list = conf.CODE_LIST
        self.__loger.info('Client %s:%s is connect the server' %self.client_address)
        while  True:
            try:
                data = mylib.b2s(self.request.recv(1024))
            except socket.error as e:
                self.__loger.info('Has lost client %s:%s' %self.client_address)
                break
            if not data:
                self.__loger.info('Has lost client %s:%s' %self.client_address)
                break     #如果收不到客户端数据了（代表客户端断开了），就断开
            self.instruction_allowcation(data) #客户端发过来的数据统一交给功能分发器处理

    def instruction_allowcation(self, instructions):
        instructions = instructions.split("|")
        function_str = instructions[0] # 客户端发过来的指令中,第一个参加都必须在服务器端有相应的方法处理
        if hasattr(self, function_str):
            func = getattr(self, function_str)
            self.__loger.info('recv instruction %s from client [%s]!' %(instructions, self.client_address))
            print(instructions)
            func(instructions)
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
            self.__current_path = tmp_path.replace('\\', '/')
            response_code = '500'
        else:
            response_code = '303'
        self.request.send(mylib.s2b('{"code":"%s", "path":"%s"}' %(response_code, self.__current_path.replace(self.__home_path, ""))))

    def get(self, instructions):
        import os
        import json
        res = json.loads(instructions[1])
        print(res)
        filename = os.path.join(self.__current_path, res['filename']).replace('\\', '/')
        print(filename)
        if os.path.isfile(filename):
            md5 = mylib.get_file_md5(filename)
            file_size = os.path.getsize(filename)
            self.request.send(mylib.s2b('ready|{"filesize":%s, "md5": "%s"}' %(file_size, md5)))
            f = open(filename, 'rb')
            send_size = res['sendsize']
            f.seek(send_size)
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
        import json
        import os
        res = json.loads(instructions[1])
        user = self.__users.get_user(res['username']) # 通过用名获取用户信息

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
        import os
        import json
        #res = self.request.recv(200)
        #print(res)
        print(type(json.loads(instructions[1])))
        print(json.loads(instructions[1]))
        res = json.loads(instructions[1])
        file_name = os.path.join(self.__current_path, res['filename'])
        md5 = res['md5']
        tmp_file_name = os.path.join(self.__current_path, '%s.ftp' %res['filename'])
        if os.path.isfile(tmp_file_name):
            tmp_file_size = os.path.getsize(tmp_file_name)
        else:
            tmp_file_size = 0
        self.request.send(mylib.s2b(r'ready|{"recv_size":%s}' %tmp_file_size))
        recv_size = tmp_file_size
        file_size = res['file_size']
        f = open(tmp_file_name, 'ab')
        self.__loger.info('Begin recv file  %s from client [%s]' %(file_name, self.client_address))
        while recv_size != file_size:
            try:
                data = self.request.recv(conf.FILE_PER_SIZE)
                recv_size += len(data)
                f.write(data)
                mylib.process_bar(recv_size, file_size)
                #print(recv_size, file_size)
            except socket.error as e:
                print(self.__code_list['306'])
                f.close()
                break
            except IOError as e:
                print(self.__code_list['305'])
        f.close()
        self.__loger.info('End recv file  %s from client [%s]' %(file_name, self.client_address))
        new_md5 = mylib.get_file_md5(tmp_file_name)
        self.__loger.info('Begin validate md5 [%s]' %tmp_file_name)
        if new_md5 == md5:
            import shutil
            shutil.move(tmp_file_name, file_name)
            self.request.sendall(mylib.s2b('308'))
            self.__loger.info('%s %s' %(self.__code_list['308'], tmp_file_name))
        else:
            os.remove(tmp_file_name)
            self.request.sendall(mylib.s2b('309'))
            self.__loger.info('%s %s' %(self.__code_list['309'], tmp_file_name))
        print(md5, new_md5)
        self.__loger.info('End validate md5 [%s]' %tmp_file_name)




    def checkspacesize(self, instructions):
        '''
        检查剩余空间是否可以上传文件方法
        :param client_cmd: 用户命令
        :return: 无
        '''
        #file_size = int(client_cmd[0]) # 获取文件大小
        # 获取剩余空间大小
        import subprocess
        cmd_call = subprocess.Popen('du -s %s' %self.__home_path, shell = True, stdout = subprocess.PIPE)
        res = cmd_call.stdout.read()
        #print(mylib.get_dir_size_for_linux(self.__home_path))

        #free_size = int(self.__current_user.get_quota() * 1024 * 1024  - mylib.get_dir_size_for_linux(self.__home_path))

        # 判断剩余空间是否够，如果够告诉客户端can，如果不够告诉客户端not
        free_size = self.__current_user.get_quota() * 1024 * 1024 - int(mylib.b2s(res).split()[0])
        self.request.send(mylib.s2b(r'{"freesize":"%s"}' %free_size))


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