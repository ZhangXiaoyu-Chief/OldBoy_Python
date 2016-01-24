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
    names = iter(['alex', 'jack', 'list'])
    print(names)
    print(names.__next__()) # 2.7 names.next()
    print(names.__next__())
    print(names.__next__())
    print(names.__next__()) # 生成的迭代对象只有3个元素，如果继续使用next方法，将会报错


    f = open('xxx.log') # f就是迭代器对象
    f.read() # 将整个文件读到内存中，非迭代器
    f.readlines() # 将整个文件读到内存中，非迭代器

    for line in f: # 将文件一行一行读到内存中，迭代器
        print(line)