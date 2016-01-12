#!/usr/bin/env python3
# coding:utf-8

from utility.MyFileHelper import MyFileHelper
from utility.MyHelper import MyHelper

class goods(object):
    def __init__(self, file):
        self.__helper = MyFileHelper(file)
        self.__all_list = self.__helper.getdict()

    def getfile(self):
        return  self.__helper.getfile()

    def print_goods_list(self):
        #print(self.__all_list)
        print('+%s+' %('-'*70))
        print('| %s%s%s%s |' %(MyHelper.alignment('编号',8, 'left'), MyHelper.alignment('名称',40, 'left') , MyHelper.alignment('价格', 10, 'left'), MyHelper.alignment('分类',10, 'left')))
        print('+%s+' %('-'*70))
        province_list = sorted(self.__all_list.items(), key = lambda d:int(d[0]))
        #print(province_list)
        for goods in province_list:
            print('| %s%s%s%s |' %(MyHelper.alignment(goods[0],8, 'left'),MyHelper.alignment(goods[1][0],40, 'left'), MyHelper.alignment(goods[1][1],10, 'left'),MyHelper.alignment(goods[1][2],10, 'left')))
        print('+%s+' %('-'*70))