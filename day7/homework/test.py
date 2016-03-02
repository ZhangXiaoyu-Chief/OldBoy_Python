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
from time import sleep

output = sys.stdout
for count in range(0,100):
    second = 1

    sleep(second)
    output.write('#')
    output.flush()
