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

class Foo(object): # Foo为类名，括号内的表示是这个类继承自哪个类，这里的object是所有类的基类，一个类可以继承自多个类
    '''
    类的说明文档，Python会自动将这里面内容赋值给类的变量__doc__
    '''
    var1 = 'var1' # 类的变量它属于类本身，而不是类的对象

if __name__ == '__main__':
    a = Animal('Dog')
    Animal.talk()
    print(a.__class__)
    print(a.__module__)
    print(a)
    print(a.__doc__)
    print(Animal.__doc__)
