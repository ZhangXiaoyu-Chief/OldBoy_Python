#!/usr/bin/env python
# coding:utf-8
import conf
from libs import mylib

class role(object):
    def __init__(self, name):
        self.name = name

    def say(self, msg):
        return input('%s: %s' %(self.name, msg))

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
        #self.name = leading_role_info['name']
        self.cash = leading_role_info['cash']
        self.deposit = leading_role_info['deposit']
        self.debt = leading_role_info['debt']
        self.hp = leading_role_info['hp']
        self.rp = leading_role_info['rp']
        self.level = leading_role_info['level']
        self.ndays = leading_role_info['ndays']
        self.goods_list = leading_role_info['goods_list']
        self.max_goods_list = leading_role_info['max_goods_list']
        self.goods_count = 0

    def get_name(self):
        return self.name
    def get_info(self):
        # print('ss')
        role_info = (self.name, self.hp, self.rp, self.cash, self.deposit, self.debt, self.level[0], self.level[1], self.level[2], self.ndays)
        return role_info
    def think(self, msg):
        input(mylib.color(msg, 32))

    def get_goods_count(self):
        return self.max_goods_list - self.goods_count
    def get_cash(self):
        return self.cash

    def buy_goods(self, goods_name, count, price):
        pass
        for goods in self.goods_list:
            if goods['name'] == goods_name:
                goods['count'] += count
                break
        else:
            tmp_goods = {}
            tmp_goods['name'] = goods_name
            tmp_goods['count'] = count
            self.goods_list.append(tmp_goods)
        self.goods_count += count
        self.cash -= price



