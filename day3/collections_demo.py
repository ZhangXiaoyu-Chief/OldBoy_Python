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
    import collections
    obj = collections.Counter('adsfasdfasdfwerwqexzcvz')
    print(obj)
    print(obj.most_common()) # 返回
    print(obj.most_common(3))
    for key, value in obj.items():
        print(key, value)
    for i in obj:
        print(i)
    for i in obj.elements():
        print(i)
    print(obj['a'])



    dic = {'a':1, 'b':2, 'c':3}
    dic1 = collections.OrderedDict(dic)
    dic2 = collections.OrderedDict(dic)
    print(dic1)
    print(dic2)
    print(id(dic1))
    print(id(dic2))

    dic = collections.defaultdict(list)
    dic['k1'].append('zhang')
    print(dic)


    MytupleClass = collections.namedtuple('MytupleClass',['x', 'y', 'z'])

    mytup = MytupleClass(11,22,33)
    print(mytup)
    print(mytup.x)
    print(mytup.y)
    print(mytup.z)


    d = collections.deque()

    d.append('1')
    d.appendleft('10')
    d.append('1')
    print(d)
    print(d.count('1'))


    import Queue
    print(Queue)

