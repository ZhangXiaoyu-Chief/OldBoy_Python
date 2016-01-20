#!/usr/bin/env python3
# coding:utf-8

from utility.MyFileHelper import MyFileHelper
import conf
import collections
import re

class haproxy(object):
    def __init__(self, file):
        self.__helper = MyFileHelper(file)
        #self.__all = self.__helper.get_all()
        self.__backends = self.__get_backends()

    def getfile(self):
        return self.__helper.getfile()

    def get_conf(self):
        return self.__helper.get_all()

    def __get_backends(self):
        all_lines = self.__helper.get_all()
        backends_list = []
        for line in all_lines:
            line = line.strip()

            if line.startswith('backend'):

                backend_name = line.split()[1]
                temp_dict = collections.OrderedDict()
                temp_dict['backend'] = backend_name
                temp_dict['record'] = []
                backends_list.append(temp_dict)

            if line.startswith('server'):
                tmp_list = line.split()
                tmp_dic = collections.OrderedDict()
                tmp_dic['server'] = tmp_list[2]
                for i in range(3,len(tmp_list),2):
                    tmp_dic[tmp_list[i]] = tmp_list[i+1]
                temp_dict['record'].append(tmp_dic)
        return backends_list

    def get_backend(self, backend_name):
        backends = self.__backends
        #print(backends)
        for backend in backends:
            if backend['backend'] == backend_name:
                return backend['record']
        else:
            return {}
    def check_record_option_key(self, op_keys):
        return not(set(list(op_keys)).difference(set(conf.record_op_list))  or 'server' not in op_keys)

    def check_record_option_type(self, records):
        for key in records.keys():
            #print(type(conf.record_op[key]), type(records[key]))
            if type(conf.record_op[key]) != type(records[key]):
                return False
        return True

    def check_ip(self,ip_str):
        return re.match('(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$',ip_str)

    def add_record(self,backend_name, record):
        backends = self.__backends
        for backend in backends:
            if backend['backend'] == backend_name:
                for rec in backend['record']:
                    if rec['server'] == record['server']:
                        backend['record'][backend['record'].index(rec)] = record
                        #rec = record
                        break
                else:
                    backend['backend'].append(record)
                break
        else:
            tmp_dict = collections.OrderedDict()
            tmp_dict['backend'] = backend_name
            tmp_dict['record'] = [record]
            backends.append(tmp_dict)
    def get_backends(self):
        return self.__backends

    def write_to_file(self):
        return True