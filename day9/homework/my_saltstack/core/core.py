#!/usr/bin/env python3
# coding:utf-8

import paramiko
import yaml
from conf import conf
from multiprocessing import Process,Pool, Queue, freeze_support

import yaml

def run(args):
    import sys
    import os
    # print(args)
    if not os.path.isfile(conf.HOSTS_FILE):
        error_msg = 'Host file %s is not exits !' %conf.HOSTS_FILE
        callback('error|%s' %error_msg)
        print(error_msg)
        exit(1)
    f = open(conf.HOSTS_FILE, 'r')
    # print(conf.HOSTS_FILE)
    data = f.read()
    f.close()
    # print(yaml.load(data))
    try:
        all_hosts = yaml.load(data)
    except Exception as e:
        error_msg = 'Option of host file %s options is error !' %conf.HOSTS_FILE
        callback('error|%s' %error_msg)
        print(error_msg)
        exit(1)
    try:
        if os.path.isfile(args[1]):
            f = open(args[1], 'r')
            data = f.read()
            data = yaml.load(data)
            for group, item in data.items():
                # print(group)
                # print(item)
                hosts = []
                for host_name in item['hosts']:
                    host = {}
                    host['hostname'] = host_name
                    host['username'] = all_hosts[host_name]['username']
                    host['password'] = all_hosts[host_name]['password']
                    host['port'] = all_hosts[host_name]['port']
                    hosts.append(host)
                # print(hosts)

                for action_list in item['actions']:
                    #print(action_list)
                    for action, options in action_list.items():
                        # action_distribute(action, hosts, options)
                        # print(action, hosts, options)
                        action_distribute(action, hosts, options)
        else:
            error_msg = 'File %s is not exit!' %args[1]
            callback('error|%s' %error_msg)
            print(error_msg)
            exit(1)
    except KeyError as e:
        error_msg = 'Option of host file %s options is error !' %args[1]
        callback('error|%s' %error_msg)
        print(error_msg)
        exit(1)
    except Exception as e:
        print(e)

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
            root_logger.error(msg)
    except IOError as e:
        print(e)

def action_distribute(action, hosts, options):
    try:
        action = action.split('.')
        if len(action) != 2:
            raise ImportError
        model_name = action[0]
        func_name = action[1]
        # print(model_name, func_name, options)
        model_obj = __import__("module.%s" %model_name)
        model_obj = getattr(model_obj, model_name)
        func = getattr(model_obj, func_name)
        # print(model_obj, func)
        freeze_support()
        pool = Pool(conf.MULT_NUM) # 定义进程池子
        for host in hosts:
             pool.apply_async(func = func, args = (host ,options, ), callback = callback )
        pool.close()
        pool.join()
    except ImportError as e:
        error_msg = 'Module is not exit!'
        callback('error|%s' %error_msg)
        print(error_msg)
        exit(1)
    except AttributeError as e:
        error_msg = 'Function is not exit!'
        callback('error|%s' %error_msg)
        print(error_msg)
        exit(1)

