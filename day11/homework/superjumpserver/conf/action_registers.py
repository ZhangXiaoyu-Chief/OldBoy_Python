#!/usr/bin/env python3
# coding:utf-8
from views import views
'''
认证模块，所有通过命令行参数调用的方法需要现在此认证方可调用
'''
actions = {
    'start': views.start,
    'stop': views.stop,
    'init_database' : views.init_database,
    'import_hosts' : views.import_hosts,
    'import_remoteusers' : views.import_remoteusers,
    'import_groups' : views.import_groups,
    'import_users' : views.import_users,
}