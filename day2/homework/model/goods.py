#!/usr/bin/env python3
# coding:utf-8
'''
商品模块
'''
from utility.MyFileHelper import MyFileHelper
# from utility.MyHelper import MyHelper

# 定义商品类
class goods(object):
    def __init__(self, file):
        '''
        构造方法
        :param file: 商品信息文件地址
        :return: 商品对象
        '''
        self.__helper = MyFileHelper(file) # 获取商品的文件helper
        #self.__all_goods = self.__helper.getlist() # 通过调用文件helper的getlist方法获取所有商品
        self.__all_goods_list = [] # 初始话所有商品信息的列表，每个元素是一个列表
        self.__shopping_cart = [] # 初始化购物车列表

        for goods in self.__helper.getlist(): # 遍历商品列表
            temp_dict = {} # 定义临时列表
            temp_dict['id'] = goods[0]
            temp_dict['name'] = goods[1]
            temp_dict['price'] = goods[2]
            temp_dict['class'] = goods[3]

            self.__all_goods_list.append(temp_dict) # 将临时字典追加到商品信息中

    # def getfile(self):
    #     return  self.__helper.getfile()

    def get_all_list(self):
        '''
        获取所有商品信息方法
        :return: 返回所有商品信息
        '''
        return self.__all_goods_list



    def add_to_shopping_cart(self, gid):
        '''
        添加购物车方法
        :param gid: 商品id
        :return: 无
        '''
        temp_dict = {}
        for one_goods in self.__shopping_cart:# 遍历所有购物车的商品
            if one_goods['id'] == gid: # 判断是否存在商品
                one_goods['num'] += 1 # 数量加1
                one_goods['subtotal'] += int(one_goods['price']) # 小计累加
                break # 退出遍历
        else:
            # 正常遍历结束，说明商品不存在于购物车内
            # 将历史字典用于保存购物车一个条目
            temp_dict['id'] = gid
            temp_dict['name'] = self.__all_goods_list[int(gid)-1]['name']
            temp_dict['price'] = int(self.__all_goods_list[int(gid)-1]['price'])
            temp_dict['num'] = 1
            temp_dict['subtotal'] = temp_dict['price']
            self.__shopping_cart.append(temp_dict) # 降临时字典最佳到购物车列表

    def get_shopping_gid(self):
        '''
        获取购物车商品id方法
        :return: 返回购物车内商品的id列表
        '''
        gid_list = []
        for one_goods in self.__shopping_cart: # 遍历购物车条目
            gid_list.append(one_goods['id']) # 将购物车条目的商品id追加到列表
        return gid_list

    def del_goods_from_cart(self, gid):
        '''
        删除购物车商品方法
        :param gid: 要删除的商品id
        :return: 无
        '''
        for one_goods in self.__shopping_cart: # 遍历购物车
            if one_goods['id'] == gid: # 判断是否id是否等于要删除商品的id
                if one_goods['num'] == 1: # 判断是否只剩1件
                    # 只剩在1件
                    self.__shopping_cart.remove(one_goods) # 删除整个条目
                    break
                else:
                    # 否则就是剩余多件
                    one_goods['num'] -= 1 # 商品数量减1
                    one_goods['subtotal'] -= int(one_goods['price']) # 小计递减
                    break
        else:
            print('输入错误或商品编号不存在')

    def get_shopping_cart(self):
        '''
        获取购物车所有信息列表
        :return: 返回购物车列表
        '''
        return self.__shopping_cart

    def del_all_cart(self):
        '''
        清空购物车方法
        :return: 无
        '''
        self.__shopping_cart = []