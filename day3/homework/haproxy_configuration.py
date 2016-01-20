#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2015年12月29日

@author: 张晓宇

Email: 61411916@qq.com

Version: 

Description: 

Help:
'''
from model.haproxy import haproxy
import conf
import collections
def print_main_menu(items):
    menu = enumerate(items, 1)
    print('-'*30)
    for menu_item in menu:
        print('%s、%s' %menu_item)
    print('-'*30)

def record_to_str(record):
    keys = list(record)
    server = '%s%s %s %s' %(' '*conf.indentation, 'server', record[keys[0]], record[keys[0]])
    for k in keys[1:]:
        server = '%s %s %s' %(server, k, record[k])
    return server

def find_backend_record():
    flag = True
    while flag:
        backend_name = input("请输入backend（r返回上级菜单）：").strip()
        records = haproxy.get_backend(backend_name)
        print(records)
        if backend_name == 'r':
            flag = False
        else:
            if records:
                for record in records:
                    # keys = list(record)
                    # server = '    %s %s %s' %('server', record[keys[0]], record[keys[0]])
                    # for k in keys[1:]:
                    #     server = '%s %s %s' %(server, k, record[k])
                    server = record_to_str(record)
                    print(server)
            else:
                print('没有找到，请检查输入是否正确')
            input('输入任意键继续')

def get_backend_str():
    backends = haproxy.get_backends()
    backend_str = ''
    for backend in backends:
        backend_str = ''.join([backend_str, '%s %s\n' %('backend',backend['backend'])])
        for record in backend['record']:
            server = record_to_str(record)
            backend_str = ''.join([backend_str, server, '\n'])
    return backend_str
def show_backends():
    # backends = haproxy.get_backends()
    # for backend in backends:
    #     print('%s %s' %('backend',backend['backend']))
    #     for record in backend['record']:
    #         server = record_to_str(record)
    #         print(server)
    backend_str = get_backend_str()
    print(backend_str)


def insert_backend_record():
    flag = True
    while flag:
        record = input("请输入要新加的记录（r返回上级菜单）：").strip()
        if record == 'r':
            flag = False
        else:
            import json
            try:
                tmp_dic = json.loads(record)
            except Exception:
                 input('输入的格式错误，按任意键继续')
                 continue
            record = tmp_dic.get('record')
            backend_name = tmp_dic.get('backend')
            if record and backend_name:
                #print(record)
                record_ord_dic = collections.OrderedDict()
                #print(record.keys())
                if haproxy.check_record_option_key(record.keys()) and haproxy.check_record_option_type(record):
                    if haproxy.check_ip(tmp_dic.get('record').get('server')):
                        for op in conf.record_op_list:
                            if record.get(op):
                                record_ord_dic[op] = record.get(op)
                        print(record_ord_dic)
                        haproxy.add_record(backend_name,record_ord_dic)
                    else:input('输入ip地址不合法请检查，按任意键继续')

                else:
                    input('输入record包含不合法关键字或record参数类型错误，请检查，按任意键继续')
                    # for op in conf.record_op:
                    #     #record_ord_dic[op] = record[op]
                    #     pass
                #print(record_ord_dic)
            else:
                input('输入错误，请检查json字符串的第一层key是否包含是否包含backend或record，按任意键继续')

def write_to_file():
    chose = input('确认是否将修改写入到配置文件中（y）: ')
    if chose == 'y':
        backends = haproxy.get_backends()
        backend_str = get_backend_str()
        # backend_str = ''
        # for backend in backends:
        #     backend_str = ''.join([backend_str, '%s %s\n' %('backend',backend['backend'])])
        #     for record in backend['record']:
        #         server = record_to_str(record)
        #         backend_str = ''.join([backend_str, server, '\n'])
        print(backend_str)
        if haproxy.write_to_file():
            input('已经成功将修改写入到文件')
        else:
            input('写入文件失败')


if __name__ == '__main__':
    haproxy = haproxy('haproxy.conf')
    flag = True
    while flag:
        print(conf.app_info)
        print_main_menu(conf.main_menu)
        chose = input('请输入操作编号（输入q放弃保存退出系统）').strip()
        if chose == '1':
            find_backend_record()
        elif chose == '2':
            insert_backend_record()
        elif chose == '3':
            pass
        elif chose == '4':
            write_to_file()
        elif chose == '5':
            show_backends()
            input('按任意键继续')
        elif chose == 'q':
            flag = False
        else:
            input('输入错误，按任意键继续')

