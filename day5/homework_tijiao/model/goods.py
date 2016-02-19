#!/usr/bin/env python
# coding:utf-8
import conf
import json

class goods(object):
    def __init__(self):
        self.__goods_file = conf.GOODS_FILE
        self.__all_goods = self.__read_all_goods()

    def __read_all_goods(self):
        '''
        读取所有商品
        :return: 返回所有商品列表，失败则返回None
        '''
        import codecs
        try:
            with codecs.open(self.__goods_file, 'r', 'utf-8') as f:
                all_goods = json.load(f)
            return all_goods
        except Exception:
            return None

    def get_all_goods(self):
        '''
        获取商品列表
        :return: 所有商品信息
        '''
        return self.__all_goods