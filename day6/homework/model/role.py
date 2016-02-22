#!/usr/bin/env python
# coding:utf-8
import conf


class role(object):
    def __init__(self, name):
        self.__name = name

    def say(self, msg):
        input('%s: %s' %(self.__name, msg))

# LEADING_ROLE_INIT_DATA = {
#     name:"李磊",
#     cash:1000,
#     deposit:0,
#     debt:0,
#     hp:100,
#     rp:0,
#     level:[0,0,0],
#     ndays:0,
#     goods_list:[],
#     max_goods_list:100
# }
class leading_role(role):
    def __init__(self, leading_role_info):
        super(leading_role, self).__init__(leading_role_info['name'])
        self.__cash = leading_role_info['cash']
        self.__deposit = leading_role_info['deposit']
        self.__debt = leading_role_info['debt']
        self.__hp = leading_role_info['hp']
        self.__rp = leading_role_info['rp']
        self.__level = leading_role_info['level']
        self.__ndays = leading_role_info['ndays']
        self.__goods_list = leading_role_info['goods_list']
        self.__max_goods_list = leading_role_info['max_goods_list']

    def get_name(self):
        return self.__name




