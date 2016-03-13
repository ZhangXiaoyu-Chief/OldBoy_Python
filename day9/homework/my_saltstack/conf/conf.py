#!/usr/bin/env python3
# coding:utf-8
import os
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RSA_DIR = '%s/rsas' %BASE_DIR # 秘钥文件目录

LOG_FILE = '%s/logs/my_saltstack.log' %BASE_DIR # 日志文件目录

MULT_NUM = 5 # 进程数

HOSTS_FILE = '%s/conf/hosts.conf' %BASE_DIR