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
    calculator = calculator()

    while True:
        print('请输入四则运算表达式（输入q退出程序）：')
        print('例如：1-2*((60-30+(-40/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))')
        expression = input('>> ').strip().replace(' ', '')
        # expression = '1-2*((60-30+(-40/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
        # expression = '1-2*((60-30+(-40/5)*(9-2*5.0/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
        # m = re.match('^[\+\-]{0,1}\d+[.]{0,1}\d*([\+\-\*\/]{1}[\+\-]{0,1}\d+[.]{0,1}\d*)+$', expression)
        # print(m)
        #expression = - -(1.1+1+1 -( -1) -(1+1 + (1+1+2.2))) + - - - - -111 + - - + + - - 3 - + + + + + + + - - - + - - - 1+4  + 4    /  2+(1+3)*4.1+(2-1.1)**2 /2**3

        if expression != 'q':
            #print(re.findall('[\+\-]{2,}', expression))
            result = calculator.getResult(expression)

            if result:
                print('myEval：', float(result))
                print('eval：', eval(expression))
            else:
                print('输入的的表达不合法，请检查')
            pass
        else:
            break
        input('按任意键继续')