#!/usr/bin/env python3
# coding:utf-8
from models import dbmodels
from models import dbconn
import datetime
# class AuditLog(Base):
#     __tablename__ = 'audit_log' # 表名
#     id = Column(Integer, primary_key = True) # id字段，逐渐，自增
#     userprofile_id = Column(Integer, ForeignKey('user_profile.id')) # userprofile_id字段，外键关联user_profile表id字段
#     hostuser_id = Column(Integer, ForeignKey('host_user.id')) # hostuser_id字段，外键关联host_user表id字段
#     CMD_TYPE= [
#         (u'cmd', u'CMD'),
#         (u'login', u'LOGIN'),
#         (u'logout', u'LOGOUT'),
#     ] # 选项列表
#     cmd_type = Column(ChoiceType(CMD_TYPE)) # cmd_tpye字段，只能是选项列表里规定的值
#     cmd = Column(String(255)) # cmd字段
#     data = Column(DateTime, default = datetime.now()) # data字段，日期时间列行，默认为当前时间
def insert_log(user, hostuser, cmd_type, msg):
    log = dbmodels.AuditLog(userprofile_id = user.id, hostuser_id = hostuser.id, cmd_type = cmd_type, cmd = msg, datetime = datetime.datetime.now())
    dbconn.session.add(log)
    dbconn.session.commit()
