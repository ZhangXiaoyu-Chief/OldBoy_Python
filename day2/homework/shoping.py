#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年1月12日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description:

Help:
'''
import conf
from model.goods import goods
from model.customer import customer
goods = goods(conf.goods_file)
#print(goods.get_list())
customer = customer(conf.customer_file)
print(conf.app_info)
print('请先登录：')
goods.print_goods_list()

if customer.authenticate():
    print(customer.get_current_customer_info())
    goods.print_goods_list()


