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
    import re
    s = '--(1.1+1+1-(-1)-(1+1+(1+1+2.2)))+-----111+--++--3-+++++++---+---1+4+4/2+(1+3)*4.1+(2-1.1)*2/2*3'
    def replace_sign(expression):
        '''
        替换多个连续+-符号的问题，例如+-----，遵循奇数个负号等于正否则为负的原则进行替换
        :param expression: 表达式，包括有括号的情况
        :return: 返回经过处理的表达式
        '''
        def re_sign(m):
            if m:
                if m.group().count('-')%2 == 1:
                    return '-'
                else:
                    return '+'
            else:
                return ''
        expression = re.sub('[\+\-]{2,}', re_sign, expression)
        return expression

    s = replace_sign(s)
    print(s)