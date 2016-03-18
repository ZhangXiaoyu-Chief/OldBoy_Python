#!/usr/bin/env python3
# coding:utf-8

from model import myParamiko
def run(host, option):
    # print(host)

    # print(cmd)
    try:
        cmd = option['command']
        ssh = myParamiko.get_ssh(host)
    except KeyError as e:
        error_info = 'option error'
        print(error_info)
        msg = 'error|[%s] : is fail [%s]' %(host['hostname'], error_info )
        return msg
    except Exception as e:
        msg = 'error|[%s] : [%s] is fail [%s]' %(host['hostname'], cmd, e)
        return msg
    #print(ssh)# 获取ssh对象
    stdin, stdout, stderr = ssh.exec_command(cmd) # 执行命令
    # 获取标准输出或错误输出内容
    stdout_msg = stdout.read().decode()
    stderr_msg = stderr.read().decode()

    print("[%s] : [%s]" %(host['hostname'], cmd))
    if not stderr_msg: # 如果标准错误输出内容为空说明执行成功
        print(stdout_msg)
        msg = 'info|[%s] : [%s] is successful' %(host['hostname'], cmd)
        return msg
    else:
        print(stderr_msg)
        msg = 'error|[%s] : [%s] is fail [%s]' %(host['hostname'], cmd, stderr_msg)
        return msg