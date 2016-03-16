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
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey

if __name__ == '__main__':

    metadata = MetaData() # 创建metadata对象

    # 创建user对象，对应user表
    user = Table('user', metadata,
        Column('id', Integer, primary_key = True), # Integer对应数据库的int类型primary_key=True表示是主键
        Column('name', String(20)), # String对应varchar类型，20表示长度，相当与varchar(20)
    )
    # 创建color对象，对应color表
    color = Table('color', metadata,
        Column('id', Integer, primary_key = True),
        Column('name', String(20)),
    )
    # 创建引擎对象，pymysql表示使用pymysqlapi
    engine = create_engine("mysql+pymysql://root:123.com@localhost:3306/s12", max_overflow=5)

    metadata.create_all(engine)