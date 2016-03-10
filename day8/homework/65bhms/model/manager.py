#!/usr/bin/env python
# coding:utf-8
from conf import conf
from multiprocessing import Process,Pool, Queue, freeze_support
from libs import mylib
import paramiko

def run_cmd(host, cmd):
    ssh = get_ssh(host)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout_msg = stdout.read().decode()
    stderr_msg = stderr.read().decode()

    print("[%s] : [%s]" %(host['hostname'], cmd))
    if stdout_msg:
        print(stdout_msg)
        msg = 'info|[%s] : [%s] is successful' %(host['hostname'], cmd)
        return msg
    else:
        print(mylib.color(stderr_msg))
        msg = 'error|[%s] : [%s] is fail [%s]' %(host['hostname'], cmd, stderr_msg)
        return msg

def get_file(host, cmd):
    import os
    from conf import conf
    ssh = get_ssh(host)
    src_file = cmd[0]
    dst_path = cmd[1]

    dst_path = os.path.join(dst_path, host['hostname'])
    os.mkdir(dst_path)
    print("[%s] get file: [%s]" %(host['hostname'], src_file))
    stdin, stdout, stderr = ssh.exec_command('ls -l %s' %src_file)
    if stderr.read().decode() == '':
        sftp, tran = get_sftp(host)
        dst_file = os.path.join(dst_path, os.path.split(src_file)[1])
        try:
            sftp.get(src_file, dst_file)

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
    return msg


def put_file(host, cmd):
    import os
    from conf import conf
    ssh = get_ssh(host)

    src_file = cmd[0]
    #print(src_file)
    dst_path = cmd[1]
    #print(dst_path)
    dst_file = os.path.join(dst_path, os.path.split(src_file)[1])

    #dst_path = os.path.join(dst_path, host['hostname'])
    #os.mkdir(dst_path)
    #dst_file = os.path.join(dst_path, os.path.split(src_file)[1])
    #stdin, stdout, stderr = ssh.exec_command('ls -l %s' %src_file)
    #if stderr.read().decode() == '':
    sftp, tran = get_sftp(host)
    # print(src_file)
    # print(sftp)
    try:
        sftp.put(src_file, dst_file)

        tran.close()
        success_info = 'put file %s to %s is successful' %(cmd[0], dst_file, )
        msg = 'info|[%s] : %s' %(host['hostname'], success_info)
        print(success_info)
    except Exception as e:
        error_info = e
        print(error_info)
        msg = 'error|[%s] : put file %s is fail [%s]' %(host['hostname'], cmd[0], error_info )
    return msg
    # else:
    #     error_info = conf.CODE_LIST['107'] %src_file
    #     print(error_info)
    #     msg = 'error|[%s] : put file %s is fail [%s]' %(host['hostname'], cmd[0], error_info )
    #return msg

def callback(msg):
    level,msg = msg.split('|')
    import logging
    file_handler = logging.FileHandler(conf.LOG_FILE, "a", encoding = "UTF-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", '%Y-%m-%d %H:%M:%S')

    file_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
    try:
        if level == 'info':
            root_logger.info(msg)
        elif level == 'error':
            print(level)
            root_logger.error(msg)
    except IOError as e:
        print(e)
def get_ssh(host):

    if 'password' in host.keys():
        transport = paramiko.Transport((host['hostname'], host['port']))
        transport.connect(username = host['username'], password = host['password'])

        ssh = paramiko.SSHClient()
        ssh._transport = transport
        # ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
        # ssh.connect(hostname = host['hostname'], port = host['port'], username = host['username'], password = host['passowrd'])
    else:
        private_key = paramiko.RSAKey.from_private_key_file(host['pkey'])
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = host['hostname'], port = host['port'], username = host['usrename'], pkey = private_key)
    return ssh

def get_sftp(host):
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



def mult_run(hosts, cmd, func):
    freeze_support()
    pool = Pool(conf.MULT_NUM)
    for host in hosts:
         host_info = conf.HOSTS[host]
         pool.apply_async(func = func, args = (host_info ,cmd, ), callback = callback )
    pool.close()
    pool.join()

