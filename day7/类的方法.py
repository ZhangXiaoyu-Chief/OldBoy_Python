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
    class_var1 = 'var1' # 类的变量，它属于类本身，而不是类的对象，可以通过类名.变量名的方式进行调用，也可以对象.变量名调用前提是，没有同名的对象的变量
    def __init__(self, arg, arg2):
        '''
        初始化方法，有点类似于java语言的构造方法，在创建类的对象的时候自动调用
        :param var2: 参数，初始化方法也可以
        :return:
        '''
        self.var2 = arg # 对象的变量，属于对象不属于类，只能通过对象.变量名的方式调用
        self.__var3 = arg # 对象的变量，只能在内部调用，不能通过对象.变量名的方式调用，并且不能被继承

    def func1(self, arg):
        '''
        方法
        1、方法属于类（也就是在实例化的时候不会像对象的变量一样单独开辟内存空间）
        2、self表示类的对象本身，当我们通过对象名.方法()来调用的时候，解释器会自动将对象作为第一个参数传给方法，方法名.方法(对象名)
        :return:
        '''
        # 方法体，方法体可以通过self.关键字调用对象的变量和方法
        self.__var3 = arg # 方法可以调用私有变量和方法

    def __func2(self):
        '''
        私有方法，和私有变量一样，不能被继承和外部调用
        :return:
        '''
        pass

class Foo2(Foo):
    def __init__(self, arg, arg2):
        '''
        1、这里调用了父类的初始化方法，特别注意由于“__变量名”表示的私有方法，
        2、这里尽管调用了父类的构造方法，__var3变量作为父类的私有方法，子类在没有重新定义之前依然没有这个变量，这点要特别注意
        :param arg:
        :param arg2:
        :return:
        '''
        super(Foo2, self).__init__(arg, arg2)
        self.__var3 = arg2 # 由于__var3是父类的私有方法，尽管调用了父类的初始化方法，子类依然不会有，所以依然需要重新定义


class Role(object):
    def __init__(self, name):
        self.name = name
    def get_name(self):
        return self.name
class Teacher(Role):
    def __init__(self, name, course):
        '''
        如果父类已经有一个方法，子类也有一个同名的方法，就会覆盖掉父类的方法，专业术语叫做重写
        '''
        super(Teacher, self).__init__(name) # 通过super这种语法可以调用父类的方法和变量，这里调用父类的构造方法，初始化name
        self.course = course # 这个变量是父类所没有的
    def say(self): # 定义父类的
        print('My name is %s, i am a English teather' %self.name)

class Foo(object):
    def __init__(self, count):
        self.__count = count
    @property # 属性装饰器，通过他把一个方法装饰成属性
    def count(self):
        return self.__count
    @count.setter
    def count(self, value): # 这里除了self只能有一个参数
        self.__count = value
    @count.deleter
    def count(self): # 这里除了self不能有其他参数
        del self.__count

class Foo(object):
    __name = 'name' # 私有类变量
    def __init__(self):
        self.__age # 私有成员变量
    def __funce(self): # 私有方法
        pass

class Foo(object):
    def __del__(self):
        print('del object')

class Foo(object):
    def __call__(self):
        print('__call__ is exec')

class Province(object):
    country = 'China'

    def __init__(self, name):
        self.name = name

    def func(self):
        pass

class Foo(object):
    def __str__(self):
        return 'Foo object'

class Foo(object):
    def __getitem__(self, key):
        print('__getitem__',key)

    def __setitem__(self, key, value):
        print('__setitem__',key,value

    def __delitem__(self, key):
        print '__delitem__',key

if __name__ == '__main__':
    obj = Foo()
    print(obj['ke'])


