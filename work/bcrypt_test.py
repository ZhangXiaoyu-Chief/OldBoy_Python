#!/usr/bin/env python
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 

Description: 
Help:
'''
import bcrypt
import sys
if __name__ == '__main__':
    argv = sys.argv
    if len(argv) == 2:
        s = argv[1]
        pw_hash = bcrypt.hashpw(s, bcrypt.gensalt())
        print('pwd: %s' %argv[1])
        print('pwd_hash: %s' %pw_hash)
    else:
        print('error: arg error')
