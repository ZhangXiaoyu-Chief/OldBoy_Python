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
if __name__ == '__main__':
    import configparser
    # config = configparser.ConfigParser()
    # config['dbs'] = {"host":'127.0.0.1', 'username':'root', "passord":'123.com'}
    # config['server'] = {}
    # config['server']['name'] = 'www.baidu.com'
    # config['server']['port'] = '80'
    # with open('example.ini', 'w') as configfile:
    #     config.write(configfile)
    # config = configparser.ConfigParser()
    # config.read('example.ini')
    # print(config.sections())
    # print(config['dbs']['host'])
    # sec = config.has_section('dbs')
    # print(sec)
    # sec = config.has_option('dbs', 'host')
    # print(sec)
    # config.add_section('oracle') # 添加个session，前提是session不能存在
    # config['oracle']['host'] = '192.168.1.189'
    # config.write(open('example_bak.ini', 'w'))
pass

import configparser
config = configparser.ConfigParser() # 创建configparser对象
config.read('example.ini')
# print(config.sections())
# print(config['server']['name'])
# print('server' in config)
print(config.options('dbs'))
print(config.items('dbs')) # 获取某个session的键值列表，类似字典的items方法
print(config.get('dbs', 'host')) # 获取某个session下的某个option的值
port = config.getint('server', 'port') # 获取某个session下的某个option的值，并以int的方式返回
print(port)
print(type(port))
print(config.getboolean('server', 'isdown'))
config.remove_option('dbs','host') # 删除option
config.remove_section('server') # 删除session
config.write(open('example_back.ini', 'w')) # 将config保存到文件
