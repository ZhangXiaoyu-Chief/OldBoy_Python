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

from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, func
from  sqlalchemy.orm import sessionmaker, relationship
Base = declarative_base() # 生成SqlORM的基类
#create_engine("mysql+pymysql://root:123.com@localhost:3306/s12", max_overflow=5)
engine = create_engine("mysql+pymysql://root:123.com@localhost:3306/s12", echo = True)

host_2_group = Table( 'host_2_group', Base.metadata,
    Column('host_id', ForeignKey('hosts.id'), primary_key = True),
    Column('group_id', ForeignKey('groups.id'), primary_key = True)
)
class Host(Base):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key = True, autoincrement = True)
    hostname = Column(String(64), unique = True, nullable = False)
    ip_addr = Column(String(128),unique = True, nullable = False)
    port = Column(Integer, default = 22)
    #group_id = Column(Integer, ForeignKey('groups.id'))
    groups = relationship('Group', secondary = host_2_group, backref = 'hosts')


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(64), unique = True, nullable = False)



if __name__ == '__main__':
    SessionCls = sessionmaker(bind = engine)
    session = SessionCls()
    # Base.metadata.create_all(engine) #创建所有表结构
    # g1 = Group(name = 'g1')
    # g2 = Group(name = 'g2')
    # g3 = Group(name = 'g3')
    # g4 = Group(name = 'g4')
    # session.add_all([g1, g2, g3, g4])
    # h1 = Host(hostname = 'localhost', ip_addr = '127.0.0.1', port = 22)
    # h2 = Host(hostname = 'webserver', ip_addr = '192.168.0.222', port = 22)
    # h3 = Host(hostname = 'dbserver', ip_addr = '192.168.0.3', port = 22)
    # g1 = Group(name = 'g1')
    # g2 = Group(name = 'g2')

    # session.add_all([h1, h2, h3])
    # res = session.query(Host, func.count()).group_by(Host.group_id).all()
    # print(res)
    # session.commit()
    # session.add_all([g1, g2])
    groups = session.query(Group).all()
    h1 = session.query(Host).filter(Host.hostname == 'localhost').first()
    h1.groups = groups
    session.commit()