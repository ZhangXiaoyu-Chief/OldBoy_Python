#!/usr/bin/env python
# coding:utf-8

from model.customer import customer
from libs import mylib

class shopping(object):
    def __init__(self):
        self.__current_customer = []
        self.__customer = customer()
        self.__tmp_cart = []

    def get_crurrent_customer(self):
        '''
        获取当前用户
        :return:
        '''
        return self.__current_customer

    def login(self, username, password):
        '''
        登录方法
        :param username: 用户名
        :param password: 密码
        :return: 成功返回True否则返回False
        '''
        res, msg = self.__customer.find_by_username(username)
        if res and res['password'] == mylib.jiami(password):
            self.__current_customer = res
            if self.__tmp_cart:
                for item in self.__tmp_cart:
                    self.add_to_shopping_cart(item, item['num'])
                    self.__tmp_cart = []
                self.__customer.update_customer(self.__current_customer)
            return True
        else:
            return False

    def logout(self):
        '''
        注销方法
        :return: 无
        '''
        self.__current_customer = []

    def add_to_shopping_cart(self, goods, num):
        '''
        添加购物车方法
        :param gid: 商品id
        :return: 无
        '''
        temp_dict = {}
        # 判断用户是否登录，如果登录添加到用户的购物车，如果没有登录添加到临时购物车
        if self.__current_customer:
            cart = self.__current_customer['cart']
        else:
            cart = self.__tmp_cart
        for one_goods in cart:# 遍历所有购物车的商品
            if one_goods['id'] == goods['id']: # 判断是否存在商品
                one_goods['num'] += num # 数量加1
                one_goods['subtotal'] += (float(one_goods['price']) * num) # 小计累加
                break # 退出遍历
        else:
            # 正常遍历结束，说明商品不存在于购物车内
            # 将历史字典用于保存购物车一个条目
            temp_dict['id'] = goods['id']
            temp_dict['name'] = goods['name']
            temp_dict['price'] = goods['price']
            temp_dict['num'] = num
            temp_dict['subtotal'] = float(temp_dict['price']) * num
            cart.append(temp_dict) # 将临时字典追加到购物车列表
        if self.__current_customer:
            # 如果用户登录了，将更新用户信息
            self.__customer.update_customer(self.__current_customer)

    def get_cart(self):
        '''
        获取购物车列表方法
        :return: 购物车列表
        '''
        # 判断用户是否登录，如果用户登录，返回用户的购物车，否则放回临时购物车
        if self.__current_customer:
            return self.__current_customer['cart']
        else:
            return self.__tmp_cart

    def empty_cart(self):
        '''
        清空购物车方法
        :return: 无
        '''
        # 判断用户是否登录，如果登录清空用户的购物车并更新用户信息，如果没登录，清空临时购物车
        if self.__current_customer:
            self.__current_customer['cart'] = []
            self.__customer.update_customer(self.__current_customer)
        else:
            self.__tmp_cart = []

    def del_goods_from_cart(self, gid):
        '''
        删除购物车商品方法
        :param gid: 要删除的商品id
        :return: 成功返回True，否则返回False
        '''
        if self.__current_customer:
            cart = self.__current_customer['cart']
        else:
            cart = self.__tmp_cart
        for one_goods in cart: # 遍历购物车
            if one_goods['id'] == gid: # 判断是否id是否等于要删除商品的id
                if one_goods['num'] == 1: # 判断是否只剩1件
                    # 只剩在1件
                    cart.remove(one_goods) # 删除整个条目

                else:
                    # 否则就是剩余多件
                    one_goods['num'] -= 1 # 商品数量减1
                    one_goods['subtotal'] -= int(one_goods['price']) # 小计递减
                msg = '成功删除1个%s' %one_goods['name']
                if self.__current_customer:
                    self.__customer.update_customer(self.__current_customer)
                return True, msg
        else:
            msg = '该商品不在购物车内'
            return False, msg