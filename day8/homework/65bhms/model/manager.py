#!/usr/bin/env python
# coding:utf-8
from conf import conf
class manager(object):
    def __init__(self):
        self.__groups = conf.GROPS
        self.__hosts = conf.HOSTS

    def __run_cmd(self, host):
        import paramiko