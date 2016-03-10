#!/usr/bin/env python
# coding:utf-8
from conf import conf
from multiprocessing import Process,Pool, Queue, freeze_support
from libs import mylib
import paramiko

def run_cmd(host, cmd):
    '''
    远程执行命令函数
    :param host: 主机相关参数
    :param cmd: 命令
    :return: 日志消息
    '''
    ssh = get_ssh(host) # 获取ssh对象
    stdin, stdout, stderr = ssh.exec_command(cmd) # 执行命令
    # 获取标准输出或错误输出内容
    stdout_msg = stdout.read().decode()
    stderr_msg = stderr.read().decode()

    print("[%s] : [%s]" %(host['hostname'], cmd))
    if stdout_msg: # 如果标准错误输出内容为空说明执行成功
        print(stdout_msg)
        msg = 'info|[%s] : [%s] is successful' %(host['hostname'], cmd)
        return msg
    else:
        print(mylib.color(stderr_msg))
        msg = 'error|[%s] : [%s] is fail [%s]' %(host['hostname'], cmd, stderr_msg)
        return msg

def get_file(host, arg):
    '''
    下载文件函数
    :param host: 主机信息
    :param cmd: 相关参数
    :return:
    '''
    import os
    from conf import conf
    ssh = get_ssh(host)
    src_file = arg[0] # 获取源文件
    dst_path = arg[1] # 获取目标目录

    dst_path = os.path.join(dst_path, host['hostname']) # 在目标目录后面加一以主机名命名的目录
    os.mkdir(dst_path) # 创建新的目标目录
    print("[%s] get file: [%s]" %(host['hostname'], src_file))
    stdin, stdout, stderr = ssh.exec_command('ls -l %s' %src_file) # 通过执行远端ls -l来判断远端源文件是否存在
    if stderr.read().decode() == '': # 如果没有报错信息则说明执行成功
        sftp, tran = get_sftp(host) # 创建和sftp对象和transport对象
        dst_file = os.path.join(dst_path, os.path.split(src_file)[1]) # 组成完整的目标文件
        try:
            sftp.get(src_file, dst_file) # 下载文件
            tran.close()
            success_info = 'get file %s to %s is successful' %(src_file, dst_file, )
            print(success_info)
            msg = 'info|[%s] : %s' %(host['hostname'], success_info)
        except Exception as e:
            error_info = e

            print(error_info)
            msg = 'error|[%s] : get file %s is fail [%s]' %(host['hostname'], cmd[0], error_info )
    else:
        error_info = stderr.read().decode()
        print(error_info)
        msg = 'error|[%s] : get file %s is fail [%s]' %(host['hostname'], cmd[0], error_info )
    tran.close()
    return msg


def put_file(host, arg):
    '''
    上传文件函数
    :param host: 远程主机函数
    :param arg: 参数列表
    :return: 日志信息
    '''
    import os
    # from conf import conf
    # ssh = get_ssh(host)

    src_file = arg[0]
    dst_path = arg[1]
    dst_file = os.path.join(dst_path, os.path.split(src_file)[1]) # 组装完整目标文件名

    sftp, tran = get_sftp(host)
    try:
        # 执行上传如果没有报异常说明上传成功
        sftp.put(src_file, dst_file) # 上传文件
        tran.close()
        success_info = 'put file %s to %s is successful' %(cmd[0], dst_file,)
        msg = 'info|[%s] : %s' %(host['hostname'], success_info)
        print(success_info)
    except Exception as e:
        error_info = e
        tran.close()
        print(error_info)
        msg = 'error|[%s] : put file %s is fail [%s]' %(host['hostname'], cmd[0], error_info )
    return msg


def callback(msg):
    '''
    callback函数，用于pool.apply_async的回调，主要用途是同意输出日志
    :param msg: 日志内容
    :return:
    '''
    level, msg = msg.split('|') # 由于只能有一个参数，所以都是用|分割日志级别及正文
    import logging
    file_handler = logging.FileHandler(conf.LOG_FILE, "a", encoding = "UTF-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
    try:
        if level == 'info': # 根据不同的日志级别输出日志
            root_logger.info(msg)
        elif level == 'error':
            print(level)
            root_logger.error(msg)
    except IOError as e:
        print(e)

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

def mult_run(hosts, arg, func):
    '''
    启动多进程函数
    :param hosts: 主机列表
    :param arg: 参数列表
    :param func: 子进程要执行的函数
    :return: 无
    '''
    freeze_support()
    pool = Pool(conf.MULT_NUM) # 定义进程池子
    for host in hosts:
         host_info = conf.HOSTS[host]
         pool.apply_async(func = func, args = (host_info ,arg, ), callback = callback )
    pool.close()
    pool.join()

