#!/usr/bin/env python3
# coding:utf-8
WELCOME_MSG = '''------------------ Welcome [%s] login SuperJumpserver ------------------'''
ERRORNO = {
    '1001' : 'Auth fail: wrong username or password',
    '1002' : 'Too many attempts',
    '2001' : 'Command [%s] is not exist!',
    '2002' : 'invalid option !',
    '3001' : 'Invalid usage, Usage(s): %s',
    '4001' : 'File %s is not exist!',
    '5001' : 'Connect fail!',
}
DBS = {"test" : "mysql+pymysql://root:123.com@localhost:3306/superjumpserver_test", # 测试环境数据库
       "real" : "mysql+pymysql://root:123.com@localhost:3306/superjumpserver_test", # 正式环境数据库
       }

DB = DBS['test']