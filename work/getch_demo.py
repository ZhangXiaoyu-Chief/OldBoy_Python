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
if __name__ == '__main__':
    import msvcrt
    ss = msvcrt.getwch()
    # import getpass
    # getpass.getpass()
    # import getpass
    # ss = getpass.win_getpass('sss')
    # import sys
    # ss = sys.stdin.read(1)
    ss = chr(ord(ss))
    print(ss)
    if str(ss) == b'r':
        print(True)