#!/usr/bin/env python
# coding:utf-8


import conf
import json
import re
import datetime
import time
#from libs import libs
from libs import mylib

from model.account import account



class atm(object):

    def __init__(self):
        #self.__current_account = {'mail': '61411916@qq.com', 'cardid': '123456780', 'tel': '13800138000', 'name': '张晓宇', 'balance': 13500.0,
                                  #'bill': {'bill_date':1453392000.0,'payment_date':1455033600.0,'payment': 0.0, 'balance_bf': 0.0, 'new_balance': 0.0, 'interest': 0.0, 'new_charges': 0.0}, 'error_count': 0, 'status': '正常', 'cash': 7500.0, 'transaction_detail': [{"date": "2016-02-03 16:58:13", "amount": 500, "description": "sss"}, {"date": "2016-02-03 17:22:15", "amount": 500, "description": "sss"}, {"date": "2016-02-03 17:24:08", "amount": 500, "description": "sss"}], 'address': '北京市通州区', 'max_balance': 15000, 'arrearage': 0, 'password': 'cbff36039c3d0212b3e34c23dcde1456'}
        self.__current_account = {}
        self.__account = account()

    def login(funce):
        '''
        装饰器，登陆验证
        :return: 登陆成功返回True，否则返回False
        '''
        import getpass
        def wrapper(self,*args, **kwargs):

            #print(accounts)
            if self.__current_account: # 判断是否已经登录
                return funce(self, *args, **kwargs)
            while True: # 如果没有登录执行循环
                accounts = self.__account.get_accounts()
                print(accounts)
                cardid = input('请输入卡号（输入quit退出认证）：').strip()
                #password = getpass.getpass('密码：')
                if cardid == 'quit':
                    msg = '认证失败'
                    return False, msg
                password = input('密码：').strip()
                #password = libs.pwd_input()
                res,msg = self.__account.find_by_id(cardid)

                if not res:
                    input('卡号或密码错误！！请重新输入，按任意键继续。')
                    continue
                #print(res.get('status'))
                if res.get('status') != '正常':
                    input('您的账户已经%s，请联系银行客服：95588', res.get('status'))
                    continue
                if mylib.jiami(password) == res.get('password'):
                    print('认证成功')
                    self.__current_account = res
                    return funce(self, *args, **kwargs)
                else:
                    res['error_count'] += 1 #登陆失败次数加1

                    if res['error_count'] == conf.MAX_ERROR_COUNT: # 判断是否错误次数是否达到阀值
                        #锁定用户
                        res['status'] = '锁定'
                        input('您的账户已被锁定，请联系银行客服：95588')
                    else:
                        input('卡号或密码错误！！请重新输入，按任意键继续。')
                    self.__account.update_account(res) # 保存用户信息，主要是修改次数累加和状态
        return wrapper

    @login
    def pay_api(self, description, amount):
        '''
        支付接口，用于商城调用
        :param description: 消费内容
        :param amount: 金额
        :return: 成功返回True，否则返回False
        '''
        if self.__current_account:
            if self.__current_account['balance'] > amount:
                self.__current_account['balance'] -= amount
                transaction_detail = {
                    "date" : time.time(),
                    "description" : description,
                    "amount" : amount
                }
                self.__current_account['transaction_detail'].append(transaction_detail)
                res, msg = self.__account.update_account(self.__current_account)
                if res:
                    msg = '支付成功'
                    return res, msg
            else:
                msg = '余额不足'
                return False, msg
        # print(self.__current_account['cardid'])
        # print(self.__current_account['name'])
        # print(self.__current_account['transaction_detail'])
        # print(self.__account.update_account(self.__current_account))

    @login
    def auth(self):
        return True

    @login
    def get_crurrent(self):
        return self.__current_account

    @login
    def take_cash(self, amount):
        if self.__current_account:
            if self.__current_account['cash'] >= amount and self.__current_account['balance'] >= amount:
                self.__current_account['cash'] -= amount
                self.__current_account['balance'] -= amount
                transaction_detail = {
                    "date" : time.time(),
                    "description" : '提现',
                    "amount" : amount
                }
                self.__current_account['transaction_detail'].append(transaction_detail)
                res, msg = self.__account.update_account(self.__current_account)
                if res:
                    msg = '提现成功'
                    return res, msg
            else:
                msg = '余额不足'
                return False, msg


