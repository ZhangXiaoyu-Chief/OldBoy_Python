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
    a = [[i for i in range(4)] for j in range(4)]
    data = [[4, 2, 1, 0], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    data = [[4, 2, 1, 0], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    print(a)
    # for i in array:
    #     print(i)

    # for row in range(4):
    #     for col in range(row,4):
    #         tmp = a[row][col]
    #         a[row][col] = a[col][row]
    #         a[col][row] = tmp
    #     #print(a)
    #
    # print("==============")
    # for i in a:
    #     print(i)

    for row in data: #旋转前先看看数组长啥样
        print(row)

    # print('-------------')
    # for i,row in enumerate(array):
    #
    #     for index in range(i,len(row)):
    #         tmp = array[index][i] #get each rows' data by column's index
    #         array[index][i] = array[i][index] #
    #         #print(tmp,array[i][index])  #= tmp
    #         array[i][index] = tmp
    # for r in array:print(r)




    for col in range(4):
        for row in range(col,4):
            data[col][row] , data[row][col] = data[row][col], data[col][row]
    #data.reverse()
    for row in data: #旋转前先看看数组长啥样
        row = row.reverse()
        #print(row)
    for row in data:
        print(row)