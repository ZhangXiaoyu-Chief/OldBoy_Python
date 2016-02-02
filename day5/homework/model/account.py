#!/usr/bin/env python
# coding:utf-8
import conf
import json
class account(object):
    def __init__(self):
        self.__account_file = conf.ACCOUNT_FILE
        # with open(self.__account_file, 'r') as f:
        #     self.__accounts = json.load(f)
        self.__accounts = []
        self.account_info = {
            "cardid":"123456789", # 卡号
            "password":"123.com", # 密码
            "name":"张晓宇", # 持卡人姓名
            "tel":"13800138000", # 持卡人电话
            "mail":"61411916@qq.com", # 持卡人邮件，可以考虑邮件发送账单
            "address":"北京市通州区", # 持卡人地址
            "max_balance":15000, # 最高可用余额
            "balance":15000, # 当前余额
            "cash":7500,# 提现余额
            "arrearage":0, # 欠款，用来计算利息
            "bill":{# 账单
            "new_balance":0, # 本期应还金额
            "balance_bf":0, # 上期账单金额
            "payment":0, # 上期还款金额
            "new_charges":0, # 本期账单金额
            "interest":0, # 循环利息
            "transaction_detail": [
            ],
            "status":"正常", #账户状态正常、锁定、冻结
            "error_count" : 0 #密码输入错误次数
            }
        }

    def insert_account(self, cardid, name, tel, mail, address, max_balance = 0):
        '''
        创建用户类
        :param cardid: 卡号
        :param name: 账户名
        :param tel: 联系电话
        :param mail: 电子邮件
        :param address: 地址
        :param max_balance: 最大可用额度
        :return: 成功返回True，失败返回Fasle
        '''
        if max_balance == 0:
            max_balance = conf.MAX_BALANCE
        account_info = {
            "cardid" : cardid, # 卡号
            "password" : conf.DEFAULT_PASSWORD, # 密码
            "name" : name, # 持卡人姓名
            "tel" : tel, # 持卡人电话
            "mail" : mail, # 持卡人邮件，可以考虑邮件发送账单
            "address" : address, # 持卡人地址
            "max_balance" : max_balance, # 最高可用余额
            "balance" : max_balance, # 当前余额
            "cash" : max_balance / 2,# 提现余额
            "arrearage" : 0, # 欠款，用来计算利息
            "bill" : {# 账单
                "new_balance" : 0, # 本期应还金额
                "balance_bf" : 0, # 上期账单金额
                "payment" : 0, # 上期还款金额
                "new_charges" : 0, # 本期账单金额
                "interest" : 0, # 循环利息
                },
            "transaction_detail" : [],
            "status" : "正常", #账户状态正常、锁定、冻结
            "error_count" : 0 #密码输入错误次数
            }
        self.__accounts.append(account_info)
        filestr = json.dumps(account_info, self.__account_file)
        print(json.dumps(self.__accounts))
        with open(self.__account_file, 'w') as f:
             json.dump(self.__accounts, f)
        pass
    def __read_accounts(self):
        pass

# acc = account()
# print(acc.account_info)
