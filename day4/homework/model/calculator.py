#!/usr/bin/env python3
# coding:utf-8

import re
class calculator(object):

    def __init__(self):
        '''
        构造方法
        :return:
        '''
        self.__one_parentheses_ex = '\([^\(\)]+\)' # 匹配有一个括号的，用来提取括号内的子串
        #self.__no_parentheses = '^[^\(\)]+$'
        self.__check_no_parentheses_ex = '^[\+\-]{0,1}\d+[.]{0,1}\d*([\+\-\*\/]{1}[\+\-]{0,1}\d+[.]{0,1}\d*)+$' # 检查不加括号的表达式是否合法
        #self.__multiplication_division = '[\+\-]*\d+[.]{0,1}\d+[\*\/]{1}[\+\-]*\d+[.]*\d+' # 匹配乘除法表达式
        self.__multiplication_division_ex = '[\+\-]{0,1}\d+[.]{0,1}\d*[\*\/]{1}[\+\-]*\d+[.]{0,1}\d*'
        #self.__add_sub = '[\+\-]*\d+[.]*\d*[\+\-]{1}[\+\-]*\d+[.]*\d*' # 匹配加法
        self.__add_sub_ex = '[\+\-]{0,1}\d+[.]*\d*[\+\-]+\d+[.]*\d*' #匹配加减法表达式




    def __multiplication_division(self, expression):
        '''
        逐一找出乘除法表达式，并计算出所有表达式的结果
        :param expression: 四则运算表达式
        :return: 返回所有包含乘除法的四则运算表达式，也就是说只有加减法
        '''
        res = re.search(self.__multiplication_division_ex, expression)

        result = ''
        #print(res)
        if res:
            res = res.group()
            #tmp_list = re.split()
            #num1,num2  = re.split('[\*\/]', res)
            num1, num2 = re.findall('[\+\-]{0,1}\d+[.]{0,1}\d*', res)
            #print(num1,num2)
            operate = re.search('[\*\/]', res).group()
            #print(re.split('[\*\/]', res))
            result = self.__base_arithmetic(num1, operate, num2)
            #print(result)
            #print(expression)
            #print(expression.replace(res, result))
            expression = expression.replace(res, result)
            return self.__multiplication_division(expression)
        else:
            #print(result)
            return expression
    def __add_subtraction(self, expression):
        '''
        逐一找出加减法表达式，并计算出所有表达式的结果
        :param expression:
        :return:
        '''
        expression = expression.replace('++','+').replace('+-','-').replace('--',"+").replace('-+','-')
        res = re.search(self.__add_sub_ex, expression)

        result = ''
        #print(res)
        if res:
            #res = res.group().replace('++','+').replace('+-','-').replace('--',"+").replace('-+','-')
            res = res.group()
            #tmp_list = re.split()
            #num1,num2  = re.split('[\+\-]', res)
            #print(re.split('[\+\-]', res))
            #num1, num2 = re.split('[\+\-]', res)[1:]
            #num1, num2 = re.search('[\+\-]\d+[.]*\d*', res).group()
            #print(re.findall('[\+\-]*\d+[.]*\d*', res))
            num1, num2 = re.findall('[\+\-]{0,1}\d+[.]{0,1}\d*', res)
            operate = '+'

            #print(re.split('[\*\/]', res))
            result = self.__base_arithmetic(num1, operate, num2)
            #print(result)
            #print(expression)
            #print(expression.replace(res, result))
            expression = expression.replace(res, result)
            return self.__add_subtraction(expression)
        else:
            #print(result)
            return expression


    def __four_arithmetic_operation(self, expression):
        expression = self.__multiplication_division(expression)
        #print(expression)
        return self.__add_subtraction(expression)

    def __base_arithmetic(self, num1, operate, num2):
        '''
        基本计算方法，计算两个数的加减乘除结果
        :param num1: 第一个数
        :param operate: 计算符号
        :param num2: 第二个数
        :return: 计算结果
        '''

        try:
            num1 = float(num1)
            num2 = float(num2)
        except Exception:
            #print('fff')
            return None
        if operate == '+':
            result = num1 + num2
        elif operate == '-':
            result = num1 - num2
        elif operate == '*':
            result = num1 * num2
        elif operate == '/':
            result = num1 / num2
        else:
            return None

        if result >= 0:
            return '%s%s' %('+', result)
        else:
            return str(result)
    def __parentheses(self, expression):
        res = re.search(self.__one_parentheses_ex, expression)
        if res:
            res = res.group()
            #print(expression)
            res_tmp = res.replace('(','').replace(')', '')
            result = self.__four_arithmetic_operation(res_tmp)
            # print(res)
            # print(eval(res))
            # print(result)
            # print(expression)
            expression = expression.replace(res, result)
            print(expression)
            return self.__parentheses(expression)

        else:
            return expression
        pass
    def getResult(self, expression):
        expression = self.__parentheses(expression)
        return self.__four_arithmetic_operation(expression)