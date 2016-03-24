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
import sys
from model import rpcClient
if __name__ == '__main__':
    client = rpcClient.rpcClient()
    if len(sys.argv) == 1:
        sys.stderr.write("Usage: %s [commend]\n" % sys.argv[0])
    else:
        # print(' '.join(sys.argv[1:]))
        client.call(' '.join(sys.argv[1:]))