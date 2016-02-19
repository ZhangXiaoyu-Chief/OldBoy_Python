#!/usr/bin/env python
# coding:utf-8


import conf
import time
from libs import mylib
from model.account import account



class atm(object):

    def __init__(self):
        self.__current_account = {}
        self.__account = account()
        self.__admin_login = False

    def login(funce):
        '''
        装饰器，登陆验证
        :return: 登陆成功返回True，否则返回False
        '''
        import getpass
        def wrapper(self,*args, **kwargs):

            if self.__current_account: # 判断是否已经登录
                return funce(self, *args, **kwargs)
            while True: # 如果没有登录执行循环
                cardid = mylib.validate_input(r'^\d{9}$','卡号（输入quit退出认证）: ', back_str = 'quit')
                if cardid == 'quit':
                    msg = '认证失败'
                    break
                password = getpass.getpass('密码: ').strip()
                res,msg = self.__account.find_by_id(cardid)
                if not res:
                    input('卡号或密码错误！！请重新输入，按任意键继续。')
                    continue
                if res.get('status') != '正常':
                    input('您的账户已经%s，请联系银行客服：95588' %res.get('status'))
                    continue
                if mylib.jiami(password) == res.get('password'):
                    input('认证成功，按任意键继续')
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

    def admin_login(funce):
        '''
        装饰器，后台管理员登陆验证
        :return: 登陆成功返回True，否则返回False
        '''
        import getpass
        def wrapper(self,*args, **kwargs):
            if self.__admin_login:
                return funce(self, *args, **kwargs)
            while True: # 如果没有登录执行循环
                username = input('用户名（输入quit退出）：').strip()
                if username == 'quit':
                    break
                password = getpass.getpass('密码: ').strip()
                if username != conf.ADMIN_USER:
                    input('用户名或密码错误，按任意键继续')
                    continue
                if mylib.jiami(password) == conf.ADMIN_PASSWORD:
                    input('认证成功，按任意键继续')
                    self.__admin_login  = True
                    return funce(self, *args, **kwargs)
                else:
                    input('用户名或密码错误，按任意键继续')
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

    @login
    def auth(self):
        '''
        登录验证方法，用于atm_main调用，实现启动程序后必须登录
        :return: True
        '''
        if self.__current_account:
            return True
        else:
             return False


    @login
    def get_crurrent(self):
        '''
        获取当前账户
        :return: 当前账户
        '''
        return self.__current_account

    @login
    def take_cash(self, amount):
        '''
        提取现金方法
        :param amount: 欲提现金额
        :return: 成功返回True，否则返回False 以及消息
        '''
        # 判断是否登录
        if self.__current_account:
            # 判断余额和提现余额是否够
            total = amount + amount * conf.INTEREST
            if self.__current_account['cash'] >= total and self.__current_account['balance'] >= total:
                # 余额和提现余额减少
                self.__current_account['cash'] -= total
                self.__current_account['balance'] -= amount
                # 创建提现交易记录
                transaction_detail = {
                    "date" : time.time(),
                    "description" : '提现',
                    "amount" : amount
                }
                self.__current_account['transaction_detail'].append(transaction_detail)
                interest = amount * conf.INTEREST
                transaction_detail = {
                    "date" : time.time(),
                    "description" : '手续费',
                    "amount" : interest
                }
                self.__current_account['transaction_detail'].append(transaction_detail)
                # 调用self.__account的update_account方法更新账户
                res, msg = self.__account.update_account(self.__current_account)
                if res:
                    msg = '提现成功'
                    return res, msg
                else:
                    msg = '提现失败'
                    return res, msg
            else:
                msg = '余额不足'
                return False, msg
        else:
            msg = '提现失败'
            return False, msg

    @login
    def repayment(self, amount):
        '''
        还款方法
        :param amount: 还款金额
        :return: 成功返回True，否则返回False 以及消息
        '''
        # 判断是否登录
        if self.__current_account:
            self.__current_account['balance'] += amount # 余额加上还款金额
            # 判断是否有欠款，有欠款就减少欠款金额，直到欠款为0
            if self.__current_account['arrearage'] > 0:
                if self.__current_account['arrearage'] > amount:
                    self.__current_account['arrearage'] -= amount
                else:
                    #fall = amount - self.__current_account['arrearage']
                    self.__current_account['arrearage'] = 0
                    #self.__current_account['balance'] += fall

            # 生成还款交易记录
            transaction_detail = {
                    "date" : time.time(),
                    "description" : '还款',
                    "amount" : amount
                }
            # 更新账户信息
            self.__current_account['transaction_detail'].append(transaction_detail)
            res, msg = self.__account.update_account(self.__current_account)
            if res:
                msg = '还款成功'
                return res, msg
            else:
                msg = '还款失败'
                return res, msg
        else:
            msg = '还款失败'
            return False, msg

    @login
    def transfer_accounts(self, account_b, amount):
        '''
        转账方法
        :param account_b: 另一方账户
        :param amount: 金额
        :return: 成功返回True，否则返回False 以及消息
        '''
        # 判断是否登录
        if self.__current_account:
            # 判断余额是否够
            if self.__current_account['cash'] >= amount and self.__current_account['balance'] >= amount:
                # 余额和提现余额相应减少
                self.__current_account['cash'] -= amount
                self.__current_account['balance'] -= amount
                # 生成当前账户转账支出记录
                transaction_detail = {
                    "date" : time.time(),
                    "description" : '转账支出',
                    "amount" : amount
                }
                # 更新当前账户
                self.__current_account['transaction_detail'].append(transaction_detail)
                res, msg = self.__account.update_account(self.__current_account)
                if res:
                    # 另一个账户流程同还款流程
                    if account_b['arrearage'] > 0:
                        if account_b['arrearage'] > amount:
                            account_b['arrearage'] -= amount
                        else:
                            #fall = amount - account_b['arrearage']
                            account_b['arrearage'] = 0
                            #account_b['balance'] += fall

                    account_b['balance'] += amount
                    # 另个账户生成转账收入记录
                    transaction_detail = {
                            "date" : time.time(),
                            "description" : '转账收入',
                            "amount" : amount
                        }
                    account_b['transaction_detail'].append(transaction_detail)
                    # 更新另个账户信息
                    res, msg = self.__account.update_account(account_b)
                    if res:
                        msg = '转账成功'
                        return res, msg
                else:
                    msg = '转账失败'
                    return res, msg
            else:
                msg = '余额不足'
                return False, msg
        else:
            msg = '转账失败'
            return False, msg

    @admin_login
    def admin_auth(self):
        '''
        admin登录验证方法，用于atm_admin登录验证
        :return: True
        '''
        return self.__admin_login