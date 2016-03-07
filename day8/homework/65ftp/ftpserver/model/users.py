#!/usr/bin/env python
# coding:utf-8

from conf import conf
import json
class user(object):
    def __init__(self, username, password, quota):
        self.__username = username
        self.__password = password
        self.__quota = quota

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_quota(self):
        return self.__quota


class users(object):
    def __init__(self):
        self.__users_file = conf.USER_FILE
        self.__users = self.__read_users()


    def __read_users(self):
        '''
        读取所有用户信息
        :return: 返回所有用户信息列表，失败则返回None
        '''
        import codecs
        try:
            with codecs.open(self.__users_file, 'r', 'utf-8') as f:
                users = json.load(f)
            return users
        except Exception as e:
            print(e)
            return []

    def get_users(self):
        return self.__users

    def get_user(self, username):
        print(self.__users)
        for one_user in self.__users:
            if one_user['username'] == username:
                res_user = user(one_user['username'], one_user['password'], one_user['quota'])
                return res_user
        else:
            return None