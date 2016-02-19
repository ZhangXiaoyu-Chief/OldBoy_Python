#!/usr/bin/env python
# coding:utf-8


import conf
import json
import re
import libs.mylib as mylib
class customer(object):
    def __init__(self):
        self.__customer_file = conf.CUSTOMER_FILE
        self.__customers = self.__read_customers()

    def __read_customers(self):
        '''
        读取所有用户信息
        :return: 返回所有用户信息列表，失败则返回None
        '''
        import codecs
        try:
            with codecs.open(self.__customer_file, 'r', 'utf-8') as f:
                customers = json.load(f)
            return customers
        except Exception:
            return None

    def __save_customers(self):
        '''
        将用户信息列表保存至文件
        :return: 成功返回True，否则返回Fasle
        '''
        import codecs
        try:
            with codecs.open(self.__customer_file, 'w', 'utf-8') as f:
                json.dump(self.__customers, f, ensure_ascii = False, indent=4)
                return True
        except Exception:
            return False

    def __check_user(self, username):
        '''
        通过username查找查找用户
        :param username: 用户名
        :return: 存在返回该用户信息，否则返回None
        '''
        customers = self.__customers
        if customers:
            for customer in customers:
                if customer.get("username") == username:
                    return customer
            else:
                return None
        else:
            return None
    def insert_customer(self, username, password, name, tel, mail, address):
        '''
        创建用户类
        :param username: 用户名
        :param password: 密码
        :param name: 姓名
        :param tel: 联系电话
        :param mail: 电子邮件
        :param address: 地址
        :return: 成功返回True，失败返回Fasle
        '''
        if self.__check_user(username):
            # 判断用户是否存在
            msg = '用户名'
            return False, msg

        customer_info = {
            "address": address,
            "password": mylib.jiami(password),
            "username": username,
            "name": name,
            "mail": mail,
            "tel": tel,
            "cart": []
        }
        self.__customers.append(customer_info)
        if self.__save_customers():
            msg = '创建用户成功'
            return True, msg
        else:
            msg = '创建用户失败'
            self.__customers.remove(customer_info) # 保存用户失败的话，将用户从self.__accounts删除，保证文件与内存的一致
            return False, msg

    def check_username(self, username):
        '''
        检查username是否重复
        :param username: 用户名
        :return: 重复返回True，否则返回False
        '''
        customers = self.__customers
        if customers:
            for customer in customers:
                if customer.get("username") == username:
                    return True
            else:
                return False
        else:
            return False

    def get_customers(self):
        return self.__customers


    def find_by_username(self, username):
        '''
        通过卡号查找用户，用于对外调用，精确查找
        :param username: 用户名
        :return: 如果查到返回account，否则返回None
        '''
        customer = self.__check_user(username)
        if customer:
            msg = ''
            return customer, msg
        else:
            msg = '该用户名不存在'
            return None, msg


    def update_customer(self, customer):
        '''
        更新用户信息
        :param customer: 用户对象
        :return: 更新成功返回True，否则返回Fasle
        '''
        username = customer['username']
        for i in range(len(self.__customers)):
            if self.__customers[i].get("username") == username:
                old_customer = self.__customers[i]
                self.__customers[i] = customer
                if self.__save_customers():
                    msg = '修改成功'
                    return True, msg
                else:
                    msg = '修改失败'
                    self.__customers[i] = old_customer
                    return False, msg
                break
        else:
            msg = '用户不存在'
            return False, msg