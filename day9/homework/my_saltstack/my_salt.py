#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 

Description: 
Help:
'''
from core import core
import sys
if __name__ == "__main__":
    if len(sys.argv) == 2:
        core.run(sys.argv[0:])
    else:
        print('Usage: %s filename' %sys.argv[0])