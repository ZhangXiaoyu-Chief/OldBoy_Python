#!/usr/bin/env python
# coding:utf-8
import conf
import json
import libs.mylib as mylib
class account(object):
    def __init__(self):
        self.__account_file = conf.ACCOUNT_FILE
        self.__accounts = self.__read_accounts()

    def insert_account(self, cardid, name, tel, mail, address, max_balance = 0):
        '''
        创建用户类
        :param cardid: 卡号
        :param name: 账户名
        :param tel: 联系电话
        :param mail: 电子邮件
        :param address: 地址
        :param max_balance: 最大可用额度，默认值为配置文件中的MAX_BALANCE值
        :return: 成功返回True，失败返回Fasle
        '''
        if self.__check_user(cardid):
            # 判断用户是否存在
            msg = '卡号已经存在'
            return False, msg

        if max_balance == 0:
            max_balance = conf.MAX_BALANCE
        account_info = {
            "cardid" : cardid, # 卡号
            "password" : mylib.jiami(conf.DEFAULT_PASSWORD), # 密码
            "name" : name, # 持卡人姓名
            "tel" : tel, # 持卡人电话
            "mail" : mail, # 持卡人邮件，可以考虑邮件发送账单
            "address" : address, # 持卡人地址
            "max_balance" : max_balance, # 最高可用余额
            "balance" : max_balance, # 当前余额
            "cash" : max_balance / 2,# 提现余额
            "arrearage" : 0, # 欠款，用来判断是否还清欠款
            "arrearage_sum" : 0, # 欠款总额，用来计算利息
            "is_arrearage" : False,
            "bill" : {# 账单
                },
            "transaction_detail" : [],
            "status" : "正常", #账户状态正常、锁定、冻结
            "error_count" : 0 #密码输入错误次数
            }
        self.__accounts.append(account_info)
        if self.__save_accounts():
            msg = '创建用户成功'
            return True, msg
        else:
            msg = '创建用户失败'
            self.__accounts.remove(account_info) # 保存用户失败的话，将用户从self.__accounts删除，保证文件与内存的一致
            return False, msg

    def __read_accounts(self):
        '''
        读取所有用户信息
        :return: 返回所有用户信息列表，失败则返回None
        '''
        import codecs
        try:
            with codecs.open(self.__account_file, 'r', 'utf-8') as f:
                accounts = json.load(f)
            return accounts
        except Exception:
            return []

    def __check_user(self, cardid):
        '''
        通过cardid查找查找用户
        :param cardid: 卡号
        :return: 存在返回该用户信息，否则返回None
        '''
        accounts = self.__accounts
        if accounts:
            for account in accounts:
                if account.get("cardid") == cardid:
                    return account
            else:
                return None
        else:
            return None

    def __save_accounts(self):
        '''
        将用户信息列表保存至文件
        :return: 成功返回True，否则返回Fasle
        '''
        import codecs
        try:
            with codecs.open(self.__account_file, 'w', 'utf-8') as f:
                json.dump(self.__accounts, f, ensure_ascii = False, indent=4)
                return True
        except Exception:
            return False

    def check_cardid(self, cardid):
        '''
        检查cardid是否重复
        :param cardid: 卡号
        :return: 重复返回True，否则返回False
        '''
        accounts = self.__accounts
        if accounts:
            for account in accounts:
                if account.get("cardid") == cardid:
                    return True
            else:
                return False
        else:
            return False

    def find_by_id(self, cardid):
        '''
        通过卡号查找用户，用于对外调用，精确查找
        :param cardid: 卡号
        :return: 如果查到返回account，否则返回None
        '''
        account = self.__check_user(cardid)
        if account:
            msg = ''
            return account, msg
        else:
            msg = '该卡号不存在'
            return None, msg

    def find_accounts_by_cardid(self, cardid):
        '''
        通过cardid查找用户，支持模糊查找
        :param cardid: 卡号
        :return: 符合条件的用户列表，如果不存在返回空列表
        '''
        return self.__find_account(cardid)

    def find_accounts_by_name(self, name):
        '''
        通过用户名name查找用户，支持模糊查找
        :param name: 用户名
        :return: 符合条件的用户列表，如果不存在返回空列表
        '''
        return self.__find_account(name, 'name')

    def __find_account(self, findstr, key = 'cardid'):
        '''
        查找用户内部方法，支持模糊查找
        :param findstr: 查找字符串
        :param key: 字段
        :return: 返回符合条件的用户列表
        '''
        accounts = []
        if key in ['cardid', 'name']:
            for account in self.__accounts:
                if findstr in account.get(key):
                    accounts.append(account)
        return accounts

    def del_account(self, cardid):
        '''
        删除用户方法
        :param cardid: 卡号
        :return: 删除成功返回True，否则返回Fasle
        '''
        account = self.__check_user(cardid)
        if account:
            self.__accounts.remove(account)
            if self.__save_accounts():
                msg = '删除成功'
                return True, msg
            else:
                msg = '删除失败'
                self.__accounts.append(account)
                return False, msg
        else:
            msg = '卡号不存在'
            return True, msg

    def get_accounts(self):
        '''
        获取所有用户信息
        :return: 所有用户信息列表
        '''
        return self.__accounts

    def update_account(self, account):
        '''
        更新用户信息
        :param account: 用户对象
        :return: 更新成功返回True，否则返回Fasle
        '''
        cardid = account['cardid']
        for i in range(len(self.__accounts)):
            if self.__accounts[i].get("cardid") == cardid:
                old_account = self.__accounts[i]
                self.__accounts[i] = account
                if self.__save_accounts():
                    msg = '修改成功'
                    return True, msg
                else:
                    msg = '修改失败'
                    self.__accounts[i] = old_account
                    return False, msg
                break
        else:
            msg = '用户不存在'
            return False, msg

    def flush_accounts(self):
        '''
        刷新用户列表
        :return:
        '''
        self.__accounts = self.__read_accounts()