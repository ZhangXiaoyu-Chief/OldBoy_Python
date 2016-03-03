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
            try:
                # 获取用户命令
                client_cmd = mylib.b2s(conn.recv(100))
                if client_cmd == '': break
                # 将用户命令进行分割，客户端传过来的命令需要使用|分割命令本身和命令相关参数
                client_cmd = client_cmd.split("|")
                # 获取命令
                if client_cmd[0] == 'quit': # 如果是quit，退出当前循环，释放连接
                    flag = False
                    continue
                if hasattr(self, client_cmd[0]): # 根据命令执行相应的方法
                    func = getattr(self, client_cmd[0])
                    func(client_cmd)
            except Exception:
                break
        conn.close()

    def get(self, client_cmd):
        '''
        下载文件方法
        :param client_cmd: 分割后的命令
        :return: 无
        '''
        print(client_cmd)
        import os
        # 拼接目录和文件名
        filename = self.__current_path + client_cmd[1]
        # 判断文件是否存在
        if os.path.isfile(filename):
            # 获取文件的md5
            md5 = mylib.get_file_md5(filename)
            # 获取文件大小
            file_size = os.path.getsize(filename)
            # 将文件的的大小，md5以及文件准备就绪的信息通知客户端
            res = "get|ready|%s|%s" %(file_size, md5)
            self.request.sendall(mylib.s2b(res))
            f = open(filename, 'rb')
            # 获取已经传输的文件大小
            send_size = int(client_cmd[2])
            # 定位文件的位置，用于断电续传
            f.seek(send_size)
            # 判断文件是否传输完毕
            while file_size != send_size:
                # 传输读取文件内容并传输，如果剩余大小每次传输的大小，则传输固定大小，如果剩余的大小
                if file_size - send_size > conf.FILE_PER_SIZE:
                    data = f.read(conf.FILE_PER_SIZE)
                    send_size += conf.FILE_PER_SIZE
                else:
                    data = f.read(file_size - send_size)
                    send_size += (file_size - send_size)
                self.request.sendall(data)
                #print(file_size, send_size)
        else:
            res = "文件%s不存在" %filename
            self.request.sendall(mylib.s2b(res))

    def put(self, client_cmd):
        '''
        上传文件方法
        :param client_cmd: 客户端命令
        :return: 无
        '''
        import os
        import shutil
        # 拼接要上传的文件名
        filename = self.__current_path + os.path.split(client_cmd[1])[1]
        file_size = int(client_cmd[2])
        #filename = os.path.split(filename)[1]
        md5 = client_cmd[3] # 从客户端命令中获取文件的md5值，稍后用于比对
        # 定义临时文件
        tmp_filename = '%s.ftp' %filename
        # 判断临时文件是否存在，如果存在获取临时文件的大小，传给客户端，端点续传
        if os.path.isfile(tmp_filename):
            tmp_file_size = os.path.getsize(tmp_filename)
        else:
            tmp_file_size = 0
        self.request.sendall(mylib.s2b('put|ready|%s' %tmp_file_size))
        Confirm = mylib.b2s(self.request.recv(100))
        recv_size = tmp_file_size
        if Confirm.startswith('put|ready'):
            # 判断是否是续传，如果是续传文件以追加的形式打开，如果不是则以写的方式打开
            if recv_size == 0:
                f = open('%s.ftp' %filename, 'wb')
            else:
                f = open('%s.ftp' %filename, 'ab')
            # 接收文件知道传输结束
            while file_size != recv_size:
                data = self.request.recv(conf.FILE_PER_SIZE)
                # 如果传输中断，退出整个方法，这里用到了一个技巧，return一个None，强制结束
                if len(data) == 0:
                    f.close()
                    return None
                recv_size += len(data)
                f.write(data)
            f.close()
            # 对比文件md5值如果相同降临时文件重命名，否则删除
            new_md5 = mylib.get_file_md5('%s.ftp' %filename)
            if md5 == new_md5:
                shutil.move('%s.ftp' %filename, filename)
                self.request.sendall(mylib.s2b('上传成功'))
            else:
                os.remove(tmp_filename)
                self.request.sendall(mylib.s2b('上传失败'))

    def checkspacesize(self, client_cmd):
        '''
        检查剩余空间是否可以上传文件方法
        :param client_cmd: 用户命令
        :return: 无
        '''
        file_size = int(client_cmd[1]) # 获取文件大小
        # 获取剩余空间大小
        free_size = int(self.__current_user['max_size'] - mylib.get_dir_size_for_linux(self.__current_path))
        # 判断剩余空间是否够，如果够告诉客户端can，如果不够告诉客户端not
        if file_size < free_size:
            self.request.sendall(mylib.s2b('can'))
        else:
            self.request.sendall(mylib.s2b('not'))


    def auth(self, client_cmd):
        '''
        认证用户方法
        :param client_cmd: 用户命令
        :return: 无
        '''
        user = self.__userobj.get_user(client_cmd[1]) # 通过用名获取用户信息
        # 判断用户是否存在
        if user:
            # 判断密码是否正确
            if user['password'] == client_cmd[2]:
                # 如果验证当前用户等于认证成功的用户
                self.__current_user = user
                # 当前目录等于用户的家目录
                self.__current_path = user['home']
                # 告诉客户端用户成功
                self.request.sendall(mylib.s2b('ok'))
            else:
                self.request.sendall(mylib.s2b('fail'))
        else:
            self.request.sendall(mylib.s2b('fail'))

    def cd(self, client_cmd):
        '''
        cd方法，用于服务端目录切换
        :param client_cmd: 用户命令
        :return: 无
        '''
        path = client_cmd[1] # 获取cd的目录
        import os
        if path == '.': # 如果目录是.说明是当前目录，啥也不干
            pass
        elif path == '..':
            # 如果是..， 说明是父目录
            # 判断当前目录是不是已经是家目录，也就是根目录，若果是啥也不干，如果不是，进入到上一级目录
            if self.__current_path == self.__current_user['home']:
                self.request.sendall(mylib.s2b('ok'))
            else:
                self.__current_path = os.path.split(self.__current_path[0:len(self.__current_path)-1])[0] + '/'
                print(os.path.split(self.__current_path[0:len(self.__current_path)-1]))

                self.request.sendall(mylib.s2b('ok'))
        elif path == '/' or path == '~': # 如果是/或者~ 表示进入到家目录，当前目录等于用户的家目录
            self.__current_path = self.__current_user['home']
            self.request.sendall(mylib.s2b('ok'))
        else:
            # 其他情况，先判断目录是否合法，合法当前目录等于拼接后的目录，否则通知客户端目录不存在
            if os.path.isdir(self.__current_path + path):
                self.__current_path += path + '/'
                self.request.sendall(mylib.s2b('ok'))
            else:
                self.request.sendall(mylib.s2b('目录%s不存在' %path))

    def rm(self, cliend_cmd):
        '''
        删除文件方法
        :param cliend_cmd: 用户命令
        :return: 无
        '''
        filename = self.__current_path + cliend_cmd[1] # 获取要删除的文件
        import os
        import shutil
        if filename.startswith('~') or filename.startswith('/') or filename.startswith('..'):
            # 目录不合法
            self.request.sendall('目录不合法')
        elif os.path.isdir(filename):# 如果是目录递归删除目录
            shutil.rmtree(filename)
            self.request.sendall(mylib.s2b('ok'))
        elif os.path.isfile(filename): # 如果是文件，只删除文件
            os.remove(filename)
            self.request.sendall(mylib.s2b('ok'))
        else:
            # 其他情况说明文件或目录不存在
            self.request.sendall(mylib.s2b('目录或文件%s不存在' %filename))


    def ls(self, cliend_cmd):
        pass

    def move(self, cliend_cmd):
        '''
        移动文件或重命名文件方法
        :param cliend_cmd: 用户命令
        :return:
        '''
        import shutil
        import os
        # 获取旧的文件名
        filename = self.__current_path + cliend_cmd[1]
        # 获取新的文件名
        new_filename = self.__current_path + cliend_cmd[2]
        if filename.startswith('~') or filename.startswith('/') or filename.startswith('..') or new_filename.startswith('~') or new_filename.startswith('/') or new_filename.startswith('..'):
            self.request.sendall(mylib.s2b('目录不合法'))
        elif os.path.isfile(filename) or os.path.isdir(filename): # 旧的文件或目录存在执行move
            shutil.move(filename, new_filename)
            self.request.sendall(mylib.s2b('ok'))
        else:
            # 否则告诉客户端目录或文件不存在
            self.request.sendall(mylib.s2b('目录或文件%s不存在' %filename))

    def pwd(self, client_cmd):
        '''
        获取当前目录方法
        :param client_cmd: 用户命令
        :return:
        '''
        # 将当前目录告诉客户端
        self.request.sendall(mylib.s2b(self.__current_path))

    def runcmd(self, client_cmd):
        while True:
            cmd = client_cmd[1]
            cmd_call = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
            cmd_result = cmd_call.stdout.read()
            ack_msg = mylib.s2b("CMD_RESULT_SIZE|%s" %len(cmd_result))
            self.request.send(ack_msg)
            client_ack = conn.recv(50)
            if client_ack.decode() == 'CLIENT_READY_TO_RECV':
                self.request.send(cmd_result)

class myftp():
    def __init__(self):
        self.__server = socketserver.ThreadingTCPServer(conf.IP_PORT, Myserver)
    def runserver(self):
        self.__server.serve_forever()