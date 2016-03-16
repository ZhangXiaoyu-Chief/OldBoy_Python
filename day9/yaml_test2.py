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
import yaml
if __name__ == '__main__':
    doc = '''
        a: 1
        b:
            - c: 3
              f: 5
            - d: 4
'''
    f = open('test.yaml', 'r')
    print(f)
    import os
    print(os.path.isfile('test.yaml'))
    doc = f.read()
    f.close()
    print(doc)
    a = yaml.load(doc)
    print(a)