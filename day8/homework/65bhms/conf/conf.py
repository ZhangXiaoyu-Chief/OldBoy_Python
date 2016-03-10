#!/usr/bin/env python
# coding:utf-8
import os
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RSA_DIR = '%s/rsas' %BASE_DIR

LOG_FILE = '%s/logs/manager.log' %BASE_DIR

MULT_NUM = 5

GROUPS = {
    "group1":['web1'],
    "group2":['web1','web2'],
}
HOSTS = {
    "web1":{
        "hostname":"123.59.44.38",
        "username":"ubuntu",
        "password":"!Jesus@smart8345",
        "port":22,
        "pkey":os.path.join(BASE_DIR, 'id_rsa'),
    },
    "web2":
    {
        "hostname":"123.59.66.174",
        "username":"ubuntu",
        "password":"!Jesus@smart8345",
        "port":22,
    }
}


CODE_LIST = {
    "101" : "Group %s is not exit!",
    "102" : "Host is not exit!",
    "103" : "Options is error, please use -h to see the help doc!",
    "104" : "Commend execute fail",
    "105" : "Module %s is not exit!",
    "106" : "Destination file or dirctory %s is not exit!",
    "107" : "Source file or dirctory %s is not exit!",
}

# print(GROPS['group1'])
#
# for host in GROPS['group2']:
#     print(HOSTS[host])
