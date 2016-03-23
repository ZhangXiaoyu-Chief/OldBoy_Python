#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月22日

@author: 张晓宇

Email: 61411916@qq.com

Version: V1.0

Description: Redis订阅和发布演示程序，发布方
Help:
'''
from redis_helper import RedisHelper # 导入刚才定义的Redis公共类

if __name__ == '__main__':

    obj = RedisHelper() # 创建redis公共类对象
    while True:
        obj.public(input('>> ')) # 获取输入，并把输入的内容发布出去