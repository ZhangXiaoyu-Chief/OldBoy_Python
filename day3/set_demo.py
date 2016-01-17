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
    old_dict = {
        "#1":{ 'hostname':'c1', 'cpu_count': 2, 'mem_capicity': 80 },
        "#2":{ 'hostname':'c1', 'cpu_count': 2, 'mem_capicity': 80 },
        "#3":{ 'hostname':'c1', 'cpu_count': 2, 'mem_capicity': 80 }
    }


    new_dict = {
        "#1":{ 'hostname':'c1', 'cpu_count': 2, 'mem_capicity': 800 },
        "#3":{ 'hostname':'c1', 'cpu_count': 2, 'mem_capicity': 80 },
        "#4":{ 'hostname':'c2', 'cpu_count': 2, 'mem_capicity': 80 }
    }


s1 = set(old_dict)
s2 = set(new_dict)

new_list = []


new_set = s1.difference(s2)
for new_item in new_set:
    new_list.append(old_dict[new_item])

print(new_list)
print(new_set)
print(s1)