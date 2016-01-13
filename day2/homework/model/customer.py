#!/usr/bin/env python3
# coding:utf-8

from utility.MyFileHelper import MyFileHelper
import conf
class customer(object):
    def __init__(self, file):
        self.__helper = MyFileHelper(file)
        self.__password_col_num = 1
        self.__status_col_num = 2
        self.__error_count_num = 3
        self.__balance_col_num = 4
        self.__error_count_max = conf.error_count_max
        self.__current_customer_info = {}

    def __get_customer_list(self):
        return self.__helper.getdict()

    def __customer_list_to_file(self):
        self.__helper.dict_to_file(self.__customer_list)

    def get_current_customer_info(self):
        return self.__current_customer_info

    def authenticate(self):
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
        current_user =  self.__customer_list[self.__current_customer_info['username']]
        balance = int(current_user[self.__balance_col_num - 1])
        current_user[self.__balance_col_num - 1] = str(balance - total)
        self.__current_customer_info['balance'] = current_user[self.__balance_col_num - 1]
        self.__customer_list_to_file()

