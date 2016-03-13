#!/usr/bin/env python3
# coding:utf-8
import paramiko
def get_ssh(host):
    '''
    获取ssh对象函数，要求主机信息要么有password要么有key文件
    :param host: 主机信息
    :return: ssh对象
    '''
    if 'password' in host.keys(): # 如果主机有password则通过passwork的方式创建ssh对象
        transport = paramiko.Transport((host['hostname'], host['port']))
        transport.connect(username = host['username'], password = host['password'])
        ssh = paramiko.SSHClient()
        ssh._transport = transport
    else:
        # 否则通过private的方式生成ssh对象
        private_key = paramiko.RSAKey.from_private_key_file(host['pkey'])
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = host['hostname'], port = host['port'], username = host['usrename'], pkey = private_key)
    return ssh

def get_sftp(host):
    '''
    过去sftp对象函数，逻辑和get_ssh函数类似
    :param host: 主机信息
    :return: sftp对象
    '''
    if 'password' in host.keys():
        transport = paramiko.Transport((host['hostname'], host['port']))
        transport.connect(username = host['username'], password = host['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
    else:
        private_key = paramiko.RSAKey.from_private_key_file(host['pkey'])
        transport = paramiko.Transport((host['hostname'], host['port']))
        transport.connect(username = host['username'], pkey = private_key)
        sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp,transport

class src_error(Exception):
    def __init__(self, filename):
        self.__filename = filename
    def __str__(self):
        return repr('Source file or dirctory %s is not exit!' %self.__filename)

class dst_error(Exception):
    def __init__(self, filename):
        self.__filename = filename
    def __str__(self):
        return repr('Destination file or dirctory %s is not exit!' %self.__filename)
