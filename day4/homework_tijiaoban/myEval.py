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

if __name__ == '__main__':
    calculator = calculator() # 创建calculator对象
    while True:
        print('请输入四则运算表达式（输入q退出程序）：')
        print('例如：1-2*((60-30+(-40/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))')
        expression = input('>> ').strip().replace(' ', '') # 去除两边和中间的空格
        if expression != 'q':
            result = calculator.getResult(expression) # 调用calculator对象的getResult获得运算结果
            if result: # 判断结果是否为正确的结果（如果返回的数值说明表达式正确，如果返回的事False说明表达式不合法）
                print('myEval：', float(result)) # 输出结果
                print('eval：', eval(expression)) # 输出eval的结果
            else:
                print('输入的的表达不合法，请检查') # 否则提示输入不合法
            pass
        else:
            break
        input('按任意键继续')