#!/usr/bin/env python3
# coding:utf-8

from utility.MyFileHelper import MyFileHelper
import conf


class haproxy(object):
    def __init__(self, file):
        self.__helper = MyFileHelper(file)
        self.__all = self.__helper.get_all()

    def getfile(self):
        return self.__helper.getfile()

    def get_conf(self):
        return self.__helper.get_all()

    def get_backend(self):
        all_lines = self.__all
        backends_list = []
        for line in all_lines:
            line = line.strip()

            if line.startswith('backend'):

                backend_name = line.split()[1]
                temp_dict = {}
                temp_dict['backend'] = backend_name
                temp_dict['record'] = []
                backends_list.append(temp_dict)

            if line.startswith('server'):
                temp_dict['record'].append(line.split())

        for li in backends_list:
            print(li)



