#!/usr/bin/env python
# coding:utf-8

from conf import conf
import json
class users(object):
    def __init__(self):
        self.__users_file = conf.USERS_FILE
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
        except Exception:
            return []

    def get_users(self):
        return self.__users

    def get_user(self, username):
        for user in self.__users:
            if user['username'] == username:
                return user
        else:
            return {}