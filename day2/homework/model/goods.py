#!/usr/bin/env python3
# coding:utf-8

from utility.MyFileHelper import MyFileHelper
from utility.MyHelper import MyHelper

class goods(object):
    def __init__(self, file):
        self.__helper = MyFileHelper(file)
        self.__all_goods = self.__helper.getlist()
        self.__all_goods_list = []
        self.__shopping_cart = []

        for goods in self.__helper.getlist():
            temp_dict = {}
            temp_dict['id'] = goods[0]
            temp_dict['name'] = goods[1]
            temp_dict['price'] = goods[2]
            temp_dict['class'] = goods[3]
            self.__all_goods_list.append(temp_dict)

    def getfile(self):
        return  self.__helper.getfile()

    def get_all_list(self):
        return self.__all_goods_list



    def add_to_shopping_cart(self, gid):
        temp_dict = {}
        for one_goods in self.__shopping_cart:
            if one_goods['id'] == gid:
                one_goods['num'] += 1
                one_goods['subtotal'] += int(self.__all_goods_list[int(gid)-1]['price'])
                break
        else:
            temp_dict['id'] = gid
            temp_dict['name'] = self.__all_goods_list[int(gid)-1]['name']
            temp_dict['price'] = int(self.__all_goods_list[int(gid)-1]['price'])
            temp_dict['num'] = 1
            temp_dict['subtotal'] = temp_dict['price']
            self.__shopping_cart.append(temp_dict)

    def get_shopping_cart(self):
        return self.__shopping_cart

    def del_all_cart(self):
        self.__shopping_cart = []