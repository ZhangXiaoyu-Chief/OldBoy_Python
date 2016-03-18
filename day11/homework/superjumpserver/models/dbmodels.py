#!/usr/bin/env python3
# coding:utf-8
from sqlalchemy import create_engine, and_, or_, func, Table
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy import Column, Integer, String,\
    ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import ChoiceType, PasswordType
from datetime import datetime


Base = declarative_base() # 生成所有sqlorm的基类

HostUserToGroup = Table('hostuser_to_group', Base.metadata,  # 表名hostuser_to_group
    Column('hostuser_id', ForeignKey('host_user.id'), primary_key = True), # 外键关联host_user表的id字段
    Column('group_id', ForeignKey('group.id'), primary_key = True), # 外键关联group表的id字段
)

UserProfileToGroup = Table('userprofile_to_group', Base.metadata, # 表名userprofile_to_group
    Column('userprofile_id', ForeignKey('user_profile.id'), primary_key = True), # 外键关联user_profile表的id字段
    Column('group_id', ForeignKey('group.id'), primary_key = True), # 外键关联group表的id字段
)

UserProfileToHostUser = Table('userprofile_to_hostuser', Base.metadata, # 表名userprofile_to_hostuser
    Column('userprofile_id', ForeignKey('user_profile.id'), primary_key = True), # 外键关联user_profile表的id字段
    Column('hostuser_id', ForeignKey('host_user.id'), primary_key = True), # 外键关联host_user表的id字段
)

class Host(Base):
    __tablename__ = 'host' # 表名host
    id = Column(Integer, primary_key = True, autoincrement = True) # id字段，主键，自动增长
    hostname = Column(String(64), unique = True, nullable = False) # hostname字段，唯一，不能为空
    ip_addr = Column(String(64), unique = True, nullable = False) # ip_addr字段，唯一，不能为空
    port = Column(Integer, default = 22) # port字段，整形，默认22
    def __repr__(self):
        return "<Hostobject: id=%s, hostname=%s, ip_addr=%s, port=%s>" %(self.id, self.hostname, self.ip_addr, self.port)

class Group(Base):
    __tablename__ = 'group' # 表名group
    id = Column(Integer, primary_key = True) # id字段，主键，自动增长
    name = Column(String(64), unique = True, nullable = False) # name字段，唯一，不为空
    def __repr__(self):
        return "<Group object: id=%s, name=%s>" %(self.id, self.name)

class UserProfile(Base):
    __tablename__ = 'user_profile' # 表名user_profile
    id = Column(Integer, primary_key = True) # id字段，主键，自动增长
    username = Column(String(64), unique = True, nullable = False) # username字段，唯一，不为空
    password = Column(String(255), nullable = False) # password字段，不为空
    hostusers = relationship('HostUser', secondary = UserProfileToHostUser, backref = 'user_profiles') # 多对多关联HostUser表类（注意不是表名），中间表类UserProfileToHostUser（注意不是表名），反向字段为user_profiles
    groups = relationship('Group', secondary = UserProfileToGroup, backref = 'user_profiles') # 多对多关联Group表类（注意不是表名），中间表类UserProfileToGroup（注意不是表名），反向字段为user_profiles

    def __repr__(self):
        return "<UserProfile object: id=%s, username=%s>" %(self.id, self.username)

class HostUser(Base):
    __tablename__ = 'host_user' # 表名host_user
    id = Column(Integer, primary_key = True) # id字段，主键，自动增长
    host_id = Column(Integer, ForeignKey('host.id')) # host_id，外键关联host表的id字段
    AuthTypes = [
        (u'ssh-password', u'SSH/Password'),
        (u'ssh-key', u'SSH/Key'),
    ] # 选项列表
    auth_type = Column(ChoiceType(AuthTypes)) # auth_type字段，只能是选项列表里规定的值
    username = Column(String(64), nullable = True) # username字段，不为空
    password = Column(String(255)) # password字段
    host = relationship('Host', backref = 'host_users')
    groups = relationship('Group', secondary = HostUserToGroup, backref = 'host_users') # 多对多关联Group表类（注意不是表名），中间表类HostUserToGroup（注意不是表名），反向字段为host_users
    __table_args = (UniqueConstraint('host_id', 'username', name = '_host_username_uc')) # host_id和username组成联合唯一约束

    def __repr__(self):
        return "<HostUser object: id=%s, host_id=%s, username=%s>" %(self.id, self.host_id, self.username)

class AuditLog(Base):
    __tablename__ = 'audit_log' # 表名
    id = Column(Integer, primary_key = True) # id字段，逐渐，自增
    userprofile_id = Column(Integer, ForeignKey('user_profile.id')) # userprofile_id字段，外键关联user_profile表id字段
    hostuser_id = Column(Integer, ForeignKey('host_user.id')) # hostuser_id字段，外键关联host_user表id字段
    CMD_TYPE= [
        (u'cmd', u'CMD'),
        (u'login', u'LOGIN'),
        (u'logout', u'LOGOUT'),
    ] # 选项列表
    cmd_type = Column(ChoiceType(CMD_TYPE)) # cmd_tpye字段，只能是选项列表里规定的值
    cmd = Column(String(255)) # cmd字段
    datetime = Column(DateTime, default = datetime.now()) # data字段，日期时间列行，默认为当前时间

    def __repr__(self):
        return "<AuditLog object: id=%s, userprofile_id=%s, hostuser_id=%s, cmd=%s>" %(self.id, self.userprofile_id, self.hostuser_id, self.cmd)