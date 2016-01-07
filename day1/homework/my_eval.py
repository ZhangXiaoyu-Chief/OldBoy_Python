#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2015年12月30日
@author: 张晓宇
Email: 61411916@qq.com
Version: 1.0
Description: 计算器
Help:
'''

# 检查格式，如果格式正确，返回优化后的四则运算表达式，如果格式不正确返回None
def check_format(str):
    import re
    # 判断是否字符串是否有数字、+、-、*、/组成，如果有其他字符
    # print(re.search(r'([0-9\+\-\*\/]+)',str).group(0))
    # print(re.search(r'([0-9\+\-\*\/]+)',str))
    if re.search(r'([0-9\+\-\*\/]+)',str).group(0) == str:
        # print(re.search(r'[\*][\*]',str))
        # if not (re.search(r'\/\/',str) or re.search(r'\*\*',str) or re.search(r'[]\*', str)):
        # 判断是否包含+*、+/、-*、-/、**、*/、/*、//这8中非法表达式
        if not re.search(r'[\+\-\*\/][\*\/]',str):
            if re.search('\d$',str):
                return str

            else:
                return None
        else:
            return None

    else:
        return None

if __name__ == '__main__':
    a = '-1-+---3*-+--1'
    aa = check_format(a)
    if aa:
        print(aa)
    else:
        print('格式不正确，请检查')

