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
        amount -= 100
        yield 100
        print('又来？？？')
        return 1

def fib(max):
    n, a, b = 0, 0, 1
    res = []
    while n < max:
        res.append(b)
        a, b = b, a + b
        n = n + 1
    return res

def fib2(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'

if __name__ == '__main__':
    # atm = cash_money(100)
    # print(type(atm))
    # for a in atm:
    #     print(a)
    res = fib(6)
    print(res)
    for i in res:
        print(i)