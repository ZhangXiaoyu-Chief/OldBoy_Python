#!/usr/bin/env python
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description:

Help:
'''
from model.account import account
if __name__ == '__main__':
    ac = account()
    res = ac.insert_account('123456789', '张晓宇', '13800138000', '61411916@qq.com', '北京市通州区')
    print(res)