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
    import copy
    # 浅拷贝
    # copy.copy()
    # 深拷贝
    # copy.deepcopy()
    # 赋值
    # =
    # 数字和字符串的浅拷贝、深拷贝、和赋值都是引用的相同的内存地址
    a1 = 123123
    a2 = 123123
    print("id a1:",id(a1))
    print("id a2:",id(a2))

    a1 = 234234
    a2 = a1
    print("id a1:",id(a1))
    print("id a2:",id(a2))

    a3 = copy.copy(a1)
    print("id a3:",id(a3))

    a4 = copy.deepcopy(a1)
    print("id a4:",id(a4))

    n1 = {"k1":"abc", "k2":123, "k3":["abc", 123]}
    n2 = n1
    print("id n1:",id(n1))
    print("id n2:",id(n2))
    n3 = copy.copy(n1)
    print("id n3:",id(n3))
    n4 = copy.deepcopy(n1)
    print("id n4:",id(n4))
    print("id n1['k3']:",id(n1['k3']))
    print("id n2['k3']:",id(n2['k3']))
    print("id n3['k3']:",id(n3['k3']))
    print("id n4['k3']:",id(n4['k3']))


    n3['k3'][0] = 'def'
    print("n1['k3']",n1['k3'])
    print("n2['k3']",n2['k3'])
    print("n3['k3']",n3['k3'])
    print("n4['k3']",n4['k3'])


dic = {
    "cpu":[80],

}


