#!/usr/bin/env python3
# coding:utf-8
'''
客户模块
'''
from utility.MyFileHelper import MyFileHelper
import conf
class customer(object): # 定义客户类
    def __init__(self, file):
        '''
        客户类构造方法
        :param file: 客户信息文件地址
        :return: 客户类
        '''
        self.__helper = MyFileHelper(file) # 初始化文件helper
        self.__password_col_num = 1 # 定义密码所在的列
        self.__status_col_num = 2 # 定义客户状态所在的列
        self.__error_count_num = 3 # 定义最多可以操作错误的次数所在的列
        self.__balance_col_num = 4 # 定义余额所在的列
        self.__error_count_max = conf.error_count_max # 从配置文件读取最多可以输入错误多少次
        self.__current_customer_info = {} # 初始化当前用户信息

    def __get_customer_list(self):
        '''
        定义私有方法获取所有客户信息
        :return: 返回所有客户信息
        '''
        return self.__helper.getdict() # 调用文件helper的getdict方法获取所有用户信息，并返回

    def __customer_list_to_file(self):
        '''
        定义私有方法，将所有客户信息写入到文件
        :return:无
        '''
        self.__helper.dict_to_file(self.__customer_list) # 调用文件helper的dict_to_file方法将所有用户信息重新写入到文件

    def get_current_customer_info(self):
        '''
        获取当前用户信息方法
        :return: 返回当前用户信息
        '''
        return self.__current_customer_info

    def authenticate(self):
        '''
        用户认证方法
        :return: 返回布尔值，用户是否成功认证登录
        '''
        self.__customer_list = self.__get_customer_list()
        flag = True
        while flag:
            # 输入用户名
            username = input('Username(Enter quit to exit): ').strip()
            # 判断是否输入的是否为quit
            if username == 'quit':
                # 是则退出循环，返回False
                return False
            password = input('Password: ').strip()
            # 判断用户名是否存在
            if username not in self.__customer_list:
                # 不存在提示错误信息并退出当前循环让用户重新输入
                print('Error: 用户名或密码错误')
                continue
            # 判断用户是否被锁定
            if self.__customer_list[username][self.__status_col_num - 1] == 'lock':
                # 如果被锁定退出当前循环让用重新如输入
                print('Error: 您的账号已经锁定，请联系管理员')
                continue
            # 判断用户密码是否正确
            if password == self.__customer_list[username][self.__password_col_num - 1]:
                # 将用户名和余额保存自当前用户信息
                self.__current_customer_info['username'] = username
                self.__current_customer_info['balance'] = self.__customer_list[username][self.__balance_col_num - 1]
                # 正确返回True
                return True
            else:
                # 不正确
                # 提示用户名或密码错误
                print('Error: 用户名或密码错误')
                # 输入错误次数加1
                self.__customer_list[username][self.__error_count_num - 1] = str(int(self.__customer_list[username][ self.__error_count_num - 1]) + 1)
                # 判断是否已经达到3次
                if int(self.__customer_list[username][self.__error_count_num - 1]) == self.__error_count_max:
                    # 如果输入错误达到3次
                    # 提示账户将被锁定
                    print("Error: 输入错误超过%s次，账号将被锁定")
                    # 将用户状态改为lock并写入文件
                    self.__customer_list[username][self.__status_col_num - 1] = 'lock'
                    self.__customer_list_to_file()
                    break
                self.__customer_list_to_file()

    def pay(self, total):
        '''
        支付方法
        :param total: 购物总金额
        :return: 无
        '''
        current_user =  self.__customer_list[self.__current_customer_info['username']] # 获取当前用户所有信息
        balance = int(current_user[self.__balance_col_num - 1]) # 获取余额
        current_user[self.__balance_col_num - 1] = str(balance - total) # 更新当前用户余额
        self.__current_customer_info['balance'] = current_user[self.__balance_col_num - 1] # 更新self.__current_customer_info余额信息
        self.__customer_list_to_file() # 调用私有方法将更新后的所有信息写入到文件

