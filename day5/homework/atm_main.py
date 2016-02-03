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
from model.atm import atm
import libs.mylib
if __name__ == '__main__':
    ac = account()
    # res, msg = ac.insert_account('123456780', '张晓宇', '13800138000', '61411916@qq.com', '北京市通州区')
    # print(res)
    # print(msg)
    # cardid = '1234567891234567890'
    # res = ac.check_cardid(cardid)
    # print(res)
    # res,msg = ac.find_by_id('12345678011')
    # print(res)
    # print(msg)
    # res = ac.find_accounts_by_cardid('78467')
    # res = ac.find_accounts_by_name('张晓宇')
    # for i in res:
    #
    #     print(output.myfind(i.get('name'), '张晓宇'))
    # res = ac.find_accounts_by_cardid('2345')
    # for i in res:
    #
    #     print(output.myfind(i.get('cardid'), '2345'))

    # res = ac.del_account('123456789')
    # print(res)

    # atm = atm()
    # res = atm.pay_api('sss', 500)
    # print(res)
    atm = atm()
    def print_welcome():
        account = atm
        welcome_info = '''
*********************************
* %s *
* %s *
        '''
        print('*********************************')
    if atm.auth():
        print('*********************************')
