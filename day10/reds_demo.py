#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 

Description: 
Help:
'''
import redis
if __name__ == '__main__':
    pool = redis.ConnectionPool(host = '10.10.1.133', port = 6379) # 创建连接池
    r = redis.Redis(connection_pool = pool) # 创建redis对象
    pipe = r.pipeline(transaction = True) # transaction表示是否原子性执行
    r.set('name', 'alex') # 设置操作，此时应该是不执行的
    r.set('role', 'sb')
    pipe.execute() # 执行上面的所有操作
