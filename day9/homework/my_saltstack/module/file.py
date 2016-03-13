#!/usr/bin/env python3
# coding:utf-8
from model import myParamiko
'''
文件操作相关模块
'''
def get(host, option):
    '''
    下载文件函数
    :param host: 主机信息
    :param option: 相关参数
    :return: 日志消息
    '''
    #print(option)
    import os
    import time
    from conf import conf
    ssh = myParamiko.get_ssh(host)
    try:
        src_file = option['src'] # 获取源文件
        dst_path = option['dst'] # 获取目标目录
        if not os.path.isdir(dst_path): # 判断目标目录是否存在
            raise myParamiko.dst_error(dst_path) # 抛出目标不存在异常
        dst_path = os.path.join(dst_path, time.strftime("%Y%m%d%H%M%S", time.localtime())) # 生成带日期时间的目录，解决文件名重复问题
        if not os.path.isdir(dst_path): # 判断是否存在，解决多个进程创建同一个目录是的报错
            os.mkdir(dst_path)
        print("[%s] get file: [%s]" %(host['hostname'], src_file))
        stdin, stdout, stderr = ssh.exec_command('ls -l %s' %src_file)# 通过执行远端ls -l来判断远端源文件是否存在
        if stderr.read().decode() == '': # 如果没有报错信息则说明执行成功
            dst_path = os.path.join(dst_path, host['hostname']) # 在目标目录后面加一以主机名命名的目录
            os.mkdir(dst_path) # 创建新的目标目录
            sftp, tran = myParamiko.get_sftp(host) # 创建和sftp对象和transport对象
            dst_file = os.path.join(dst_path, os.path.split(src_file)[1]) # 组成完整的目标文件
            sftp.get(src_file, dst_file) # 下载文件
            tran.close()
            success_info = 'get file %s to %s is successful' %(src_file, dst_file, )
            print(success_info)
            msg = 'info|[%s] : %s' %(host['hostname'], success_info)
        else:
            raise myParamiko.src_error(src_file) # 抛出源文件不存在异常
    except KeyError as e:
        # options['src']的key错误，说明指令文件相关指令错误
        error_info = 'option error'
        print(error_info)
        msg = 'error|[%s] : get file %s is fail [%s]' %(host['hostname'], src_file, error_info )
    except (myParamiko.src_error,myParamiko.dst_error) as e:
        # 这两是自定异常，用来捕获爆出的源文件或目录不存在的异常
        error_info = e
        print(error_info)
        msg = 'error|[%s] : get file %s is fail [%s]' %(host['hostname'], src_file, error_info )
    except IOError as e:
        # 捕获文件操作异常，比如没有权限等
        error_info = e
        print(error_info)
        msg = 'error|[%s] : get file %s is fail [%s]' %(host['hostname'], src_file, error_info )
    except Exception as e:
        # 捕获其他异常
        error_info = e
        print(error_info)
        msg = 'error|[%s] : get file %s is fail [%s]' %(host['hostname'], src_file, error_info )
    return msg

def put(host, options):
    '''
    上传文件函数
    :param host: 远程主机函数
    :param options: 参数列表
    :return: 日志信息
    '''
    import os
    # from conf import conf
    # ssh = get_ssh(host)
    try:
        src_file = options['src']
        dst_path = options['dst']
        if not os.path.isfile(src_file): # 判断要上传的文件是否存在
            raise myParamiko.src_error(src_file) # 抛出源文件异常
        print("[%s] get file: [%s]" %(host['hostname'], src_file))
        dst_file = os.path.join(dst_path, os.path.split(src_file)[1]) # 组装完整目标文件名
        sftp, tran = myParamiko.get_sftp(host)
        sftp.put(src_file, dst_file) # 上传文件
        tran.close()
        success_info = 'put file %s to [%s]%s is successful' %(host['hostname'],src_file, dst_file,)
        msg = 'info|[%s] : %s' %(host['hostname'], success_info)
        print(success_info)
    except KeyError as e:
        error_info = 'option error'
        print(error_info)
        msg = 'error|[%s] : put file %s is fail [%s]' %(host['hostname'], src_file, error_info )
    except (myParamiko.src_error,myParamiko.dst_error) as e:
        error_info = e
        print(error_info)
        msg = 'error|[%s] : put file %s is fail [%s]' %(host['hostname'], src_file, error_info )
    except Exception as e:
        error_info = e
        tran.close()
        print(error_info)
        msg = 'error|[%s] : put file %s is fail [%s]' %(host['hostname'], src_file, error_info )
    return msg