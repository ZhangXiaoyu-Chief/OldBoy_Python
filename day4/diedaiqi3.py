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
def cash_money(amount):
    while amount > 0:
        pay = yield 'ajj'
        amount -= pay
        print('又来？？？')

if __name__ == '__main__':
    atm = cash_money(100)
    atm.send(50)

