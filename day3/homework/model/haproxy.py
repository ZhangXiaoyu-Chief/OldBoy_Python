#!/usr/bin/env python3
# coding:utf-8

from utility.MyFileHelper import MyFileHelper
import conf
import collections
import re

class haproxy(object):
    def __init__(self, file):
        self.__conffile = file
        self.__conffile_bak = '%s%s' %(file, '.new')
        self.__read_helper = MyFileHelper(self.__conffile)
        self.__write_helper = MyFileHelper(self.__conffile_bak)
        self.__all = self.__read_helper.get_all()
        self.__backends = self.__get_backends() # 保存从文件读出来的backend信息

    def getfile(self):
        return self.__helper.getfile()

    def get_conf(self):
        return self.__helper.get_all()

    def __get_backends(self):
        '''
        读取配置文件，从配置文件中读出backend节点的配置，并保存成有序字典
        :return: 返回处理后的backends列表
        '''
        #all_lines = self.__helper.get_all() # 调用helper的get_all()方法将配置文件全部出来
        all_lines = self.__all
        backends_list = [] # 定义用来保存所有backend信息的空列表
        for line in all_lines: # 遍历每一行
            line = line.strip()
            if line.startswith('backend'): # 判断是否是backend开头
                backend_name = line.split()[1] # 获取到backend名称
                temp_dict = collections.OrderedDict() # 创建用来保存backend信息的空的有序字典
                temp_dict['backend'] = backend_name
                temp_dict['record'] = [] # 创建用来保存每个record信息的空列表
                backends_list.append(temp_dict) # 将backend信息追加到列表

            if line.startswith('server'): # 通过判断是否为server开头判断是否是backend下面的一条记录record
                tmp_list = line.split() # 将record记录通过空格拆分
                tmp_dic = collections.OrderedDict() # 创建用来保存record信息的空有序字典
                tmp_dic['server'] = tmp_list[2] # 保存record名称
                for i in range(3,len(tmp_list),2):
                    tmp_dic[tmp_list[i]] = tmp_list[i+1] # 保存recordoptions信息
                temp_dict['record'].append(tmp_dic) # record最佳到后record列表
        return backends_list

    def get_backend(self, backend_name):
        '''
        通过backdend名获取backend信息
        :param backend_name: backend名称
        :return: 如果存在返回所有backend的record信息，如果没有找到返回空字典
        '''
        backends = self.__backends # 获取所有backend信息
        #print(backends)
        for backend in backends: # 遍历所有backend
            if backend['backend'] == backend_name: # 如果找到名称相同的返回该backend下面的record信息
                return backend['record']
        else:
            return {} # 如果没有找到返回空的字典

    def check_record_option_key(self, op_keys):
        '''
        检查新添加的添加、删除、修改等操作的record的options选项是否合法
        :param op_keys: 欲添加、删除、修改record所有的选项名称，包括server
        :return: 布尔值，如果合法返回True，否则返回Fasle
        '''
        # 通过差集判断是否存在配置文件conf.py中未定义的合法字段、另外必须包含'server'
        return not(set(list(op_keys)).difference(set(conf.record_op_list))  or 'server' not in op_keys)

    def check_record_option_type(self, records):
        '''
        检查新添加的添加、删除、修改等操作的record的options选项参数类型是否符合合法
        :param records: 欲添加、删除、修改record所有的选项的参数说着说值，不包括server
        :return: 布尔值，如果合法返回True，如果不合法返回False
        '''
        for key in records.keys(): # 遍历所有options的参数
            #print(type(conf.record_op[key]), type(records[key]))
            if type(conf.record_op[key]) != type(records[key]): # 对比参数类型，如果不合法返回Fasle
                return False
        return True # 如果遍历没有返回False说明合法，返回True

    def check_ip(self,ip_str):
        '''
        判断server参数的ip地址是否合法
        :param ip_str: ip地址
        :return: 布尔值，如果合法返回True，如果不合法返回False
        '''
        #res = re.match('(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$',ip_str) # 通过正则表达式判断ip地址是否合法

        return re.match('(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$',str(ip_str)) # 通过正则表达式判断ip地址是否合法

    def add_record(self,backend_name, record):
        '''
        添加
        :param backend_name: backend名称，表示要添加到该backend下
        :param record: # record字典
        :return:
        '''
        backends = self.__backends
        for backend in backends: # 遍历backend列表
            if backend['backend'] == backend_name: # 判断backend是否存在
                # 存在执行
                for rec in backend['record']: # 遍历所哟record
                    if rec['server'] == record['server']: # 通过server的ip的地址判断该记录是否存在
                        backend['record'][backend['record'].index(rec)] = record # 如果存在，覆盖
                        #rec = record
                        break
                else:
                    backend['backend'].append(record) # 如果不存在，追加到后面
                break
        else:
            # 如果backend不存在
            tmp_dict = collections.OrderedDict()  # 创建一个空有序字典用来保存新的backend信息
            tmp_dict['backend'] = backend_name
            tmp_dict['record'] = [record]
            backends.append(tmp_dict) # 将构建的backend追加到后面

    def get_backends(self):
        '''
        获取所有backend信息
        :return: 返回所有backend列表
        '''
        return self.__backends

    def del_record(self, backend_name, server_name):
        '''
        删除backend下面的record
        :param backend_name: backend名称
        :param server_name: record下的server的值，也就是ip地址
        :return: 布尔值，是否删除成功
        '''
        records = self.get_backend(backend_name) # 获取backend的所有记录
        if records: # 获取的不为空执行
            for record in records: # 遍历所有record
                if record['server'] == server_name: # 判断是否是要删除的记录
                    records.remove(record) # 如果是移除
                    #print(records)
                    if not records: # 判断移除后是不是为空
                        # 如果为空删除backend
                        for backend in self.__backends: # 遍历所有backend
                            if backend['backend'] == backend_name: # 判断是否为要删除的backend
                                self.__backends.remove(backend) # 移除backend
                                break
                    return True
        return False
        #print(1)

    def write_to_file(self, backend_str):
        '''
        写入文件
        :return: 写入成功返回True
        '''
        import os
        import datetime
        #file_str = conf.conf_model.format(backends = backend_str)
        #for line in self.__all
        has_write = False # 定义表示符，用来判断backend是否写入到文件
        file_str = '' # 初始化文件的内容
        for line in self.__all: # 遍历源haproxy配置文件的所有行
            if line.strip().startswith('backend') or line.strip().startswith('server'): # 判断开头是否为backend或server

                if has_write: # 判断是否已经写过backend
                    continue
                else:
                    file_str = '%s%s' %(file_str, backend_str) # 如果没写过，将当前backend所有信息写入到文件
                    #print(backend_str)
                    has_write = True # 将标识符改为Ture，说明backend已经全部写完了
            else:
                file_str = '%s%s' %(file_str, line)
                #print(line)
        # print(file_str)
        if self.__write_helper.write_all(file_str):
            # 文件完后，将当前ha_proxy文件用刚才写入的文件替换并备份
            os.rename(self.__conffile,'.'.join([self.__conffile, datetime.datetime.now().strftime('%Y%m%d%H%M%S') ]))
            # print(''.join([self.__conffile, datetime.datetime.now().strftime('%Y%m%d%H%M%S') ]))
            os.rename(self.__conffile_bak, self.__conffile)
            return True
        else:
            return False