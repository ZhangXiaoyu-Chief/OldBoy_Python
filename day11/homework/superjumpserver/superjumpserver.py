#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月28日

@author: 张晓宇

Email: 61411916@qq.com

Version: V1.0

Description: 堡垒机
1、 用户使用堡垒机用户名密码登录堡垒机
2、 不同用户拥有不同的组和不分组的远端主机权限，可以通过堡垒机登录远端主机，便于管理
3、 用户在远端主机的所有操作将被记录审计日志中，便于事后查阅分析和追究责任
Help:
'''

from conf import action_registers, conf
from libs import mylib
import sys
import os
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def help_msg():
    '''
    打印帮助信息
    :return:
    '''
    print(mylib.color('Available commands:', 32))
    for key in action_registers.actions:
        print(' ', key)
if __name__ == '__main__':
    # tty = supertty.myTty('localhost', 'zhangxiaoyu', 22, '123.com')
    # tty.run()
    argv = sys.argv # 获取命令行参数列表
    # print(sys.argv)
    # argv = ['superjumpser.py', 'import_hosts','-f', 'share/examples/hosts.json']
    # argv = ['superjumpser.py', 'init_database']
    # argv = ['superjumpser.py', 'import_remoteusers','-f', 'share/examples/hostusers.json']
    # argv = ['superjumpser.py', 'import_groups','-f', 'share/examples/groups.json']
    # argv = ['superjumpser.py', 'import_users','-f', 'share/examples/users.json']
    # argv = ['superjumpser.py', 'start']
    if len(argv) < 2: # 判断命令行参数数量是否合法
        help_msg()
        exit(1)
    if argv[1] not in action_registers.actions: # 判断命令行名命令是否在注册列表中
        mylib.print_err(conf.ERRORNO['2001'] %argv[1], quit = True)
    action_registers.actions[argv[1]](argv[1:]) # 调用注册的对应方法