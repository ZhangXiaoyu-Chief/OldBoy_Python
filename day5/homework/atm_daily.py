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

import conf
import json
import re
import libs.mylib as mylib
from model.account import account
from model.atm import atm
import time
import datetime
time.localtime()


if __name__ == '__main__':
    ac = account()
    accounts = ac.get_accounts() # 获取账户列表
    if accounts: # 判断账户列表是否存在
        for account in accounts: # 遍历账户列表
            # 判断如果用户是锁定状态，就解锁用户，并重置输入错误次数
            if account['status'] == '锁定':
                account['status'] = '正常'
                account['error_count'] = 0
            # 判断账户是否有欠款，如果有欠款就计算利息
            if account['is_arrearage']:
                # 如果有欠款就通过欠款总额计算利息
                amount = account['arrearage_sum'] * 5 / 10000
                # 生成利息记录
                transaction_detail = {
                    "date" : time.time(),
                    "description" : '利息',
                    "amount" : amount
                }
                account['transaction_detail'].append(transaction_detail)
            ac.update_account(account)
    today = time.localtime()
    # 判断今天是否是还款日
    if today.tm_mday == conf.REPAYMENT_DAY:
        if accounts:
            for account in accounts:
                # 如果欠款金额不是0也就是没有还清欠款并且欠款状态不是True
                if account['arrearage'] != 0 and not account['is_arrearage']:
                    # 将欠款状态设置为True
                    account['is_arrearage'] = True
                    if account['bill']: # 判断账单是否存在
                        if account['bill']['new_balance'] > 0: # 判断应还金额是否大于0
                            #account['arrearage'] += account['bill']['new_balance']
                            # 新的欠款总额等于原来欠款总额加上本期应还金额
                            account['arrearage_sum'] = account['bill']['new_balance']
                ac.update_account(account)

    # 判断是否是账单日
    if today.tm_mday == conf.BILL_DAY:
        if accounts:
            for account in accounts:
                if account['transaction_detail']:
                    payment = 0

                    balance_bf = 0 if not account['bill'] else account['bill']['new_balance']
                    interest = 0
                    new_charges = 0
                    day = list(time.localtime())
                    day[3:] = [0, 0, 0, 0, 0, 0] # 获取当前系统日期0点0分0秒0毫秒
                    #print(day)
                    day1 = time.mktime(tuple(day)) # 获取当前系统日期0点0分0秒0毫秒
                    day[1] -=1 # 计算1个月前的日期
                    #print(day)
                    day2 = time.mktime(tuple(day))
                    day[1] +=2 # 计算1个月前的日期
                    day[2] = conf.REPAYMENT_DAY # 日改成还款日，也就是下个月的还款日
                    #print(day)
                    day3 = time.mktime(tuple(day)) # 获取本期账单的还款日
                    for transaction in account['transaction_detail']:
                        if day2 <= transaction['date'] < day1:
                            if transaction['description'] == '还款' or transaction['description'] == '转账收入':
                                payment += transaction['amount']
                            elif transaction['description'] == '利息':
                                interest += transaction['amount']
                            else:
                                new_charges += transaction['amount']
                    account['bill']['payment'] = payment
                    account['bill']['balance_bf'] = balance_bf
                    account['bill']['interest'] = interest
                    account['bill']['new_charges'] = new_charges
                    account['bill']['new_balance'] = balance_bf - payment + new_charges + interest
                    account['bill']['bill_date'] = day1
                    account['bill']['payment_date'] = day3
                    if account['bill']['new_balance'] > 0:
                        account['arrearage'] = account['bill']['new_balance']
                    account['balance'] = account['max_balance'] - account['bill']['new_balance']
                    account['cash'] = account['max_balance'] / 2
                    #print(account)
                    ac.update_account(account)
                    # print(payment)
                    # print(balance_bf)
                    # print(interest)
                    # print(new_charges)