#!/usr/bin/env python
# coding:utf-8
import os
from model import manager
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RSA_DIR = '%s/rsas' %BASE_DIR # 秘钥文件目录

LOG_FILE = '%s/logs/manager.log' %BASE_DIR # 日志文件目录

MULT_NUM = 5 # 进程数


MODULES = {
    "cmd.run": manager.run_cmd
}


# 错误码和错误信息
CODE_LIST = {
    "101" : "Group %s is not exit!",
    "102" : "Host is not exit!",
    "103" : "Options is error, please use -h to see the help doc!",
    "104" : "Commend execute fail",
    "105" : "Module %s is not exit!",
    "106" : "Destination file or dirctory %s is not exit!",
    "107" : "Source file or dirctory %s is not exit!",
}