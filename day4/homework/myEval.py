#!/usr/bin/env python
# coding:utf-8
'''
Created on: 2016年1月24日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: 用户输入 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )
             等类似公式后，必须自己解析里面的(),+,-,*,/符号和公式，运算后得出结果，结果必须与真实的计算器所得出的结果一致

Help:
'''
from model.calculator import calculator
import re
if __name__ == '__main__':
    calculator = calculator()

    while True:
        #expression = input('请输入表达式：').strip().replace(' ', '')
        expression = '1-2*((60-30+(-40/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
        if expression != 'q':

            print('myEval：',float(calculator.getResult(expression)))
            print('eval：', eval(expression))

            pass
        else:
            break
        input('按任意键继续')