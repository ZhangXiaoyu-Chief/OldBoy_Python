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
'''
[0, 1, 2, 3]
[0, 1, 2, 3]
[0, 1, 2, 3]
[0, 1, 2, 3]

[0, 0, 0, 0]
[1, 1, 1, 1]
[2, 2, 2, 2]
[3, 3, 3, 3]
'''

# def binary_search(data_source, find_n):
#     le = len(data_source)
#     mid = int(le/2)
#     if le >= 1:
#         if data_source[mid] > find_n:
#             print('lift of %s' %data_source[mid])
#             print(data_source[:mid])
#             binary_search(data_source[:mid], find_n)
#         elif data_source[mid] < find_n:
#             print('right of %s' %data_source[mid])
#             print(data_source[mid:])
#             binary_search(data_source[mid:], find_n)
#         else:
#             print('find %s' %data_source[mid])
#     else:
#          print('not fountd')

def binary_search(data_list,find_num):
    mid_pos = int(len(data_list) /2 ) # 获取中间的索引
    mid_val = data_list[mid_pos] # 获取中间的索引对相应元素，也就是值
    print(data_list)
    if len(data_list) >1: # 递归结束条件，也就是规模绩效
        if mid_val > find_num: # 中间的值比要找的值大，说明在中间值左边
            print("[%s] should be in left of [%s]" %(find_num,mid_val))
            binary_search(data_list[:mid_pos],find_num) # 递归自己，继续查找自己的左边（也就是递归要求里的缩小调用规模）
        elif mid_val < find_num: # 中间的值比要找的值大，说明在中间值左边
            print("[%s] should be in right of [%s]" %(find_num,mid_val))
            binary_search(data_list[mid_pos + 1:],find_num)
        else: # 如果既不大于也不小于说明正好等于
            print("Find ", find_num)

    else:
        # 当列表的大小等于1的时候，不在调用自己，结束递归
        if mid_val == find_num: # 判断最用一个元素是否等于要查找的数
            print("Find ", find_num)
        else:
            print("cannot find [%s] in data_list" %find_num)

if __name__ == '__main__':
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,104]
    binary_search(primes,5)
    binary_search(primes,66)

# if __name__ == '__main__':
#     data = list(range(1, 100, 2))
#     print(data)
#     binary_search(data, 2)