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
import MySQLdb
if __name__ == '__main__':
    conn = MySQLdb.connect(host = '127.0.0.1', user = 'root', password='123.com', dbs = 's12day9')
    cur = conn.cursor()
    reCount = cur.execute('insert into sudents(name, age,sex, tel, nal)', ('Jack',22,'F', '12345', 'CH'))
    conn.commit()
    cur.close()
    conn.close()
    from salt import master
