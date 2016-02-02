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
import re
if __name__ == '__main__':
    contactInfo = 'Oldboy School, Beijing Changping Shahe: 010-8343245'
    match = re.search(r'(\w+), (\w+): (\S+)', contactInfo) #分组
    print(match)
    #match = re.search(r'(?P<last>\w+), (?P<first>\w+): (?P<phone>\S+)', contactInfo)
