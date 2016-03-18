#!/usr/bin/env python3
# coding:utf-8

from models import dbmodels, dbconn
from conf import conf
from libs import mylib
from models import auditlog

errono = conf.ERRORNO

def auth():
    '''
    身份认证函数
    :return: 成功返回True，否则返回False
    '''
    import getpass
    count = 0
    while count < 3:
        username = input('Username: ').strip() # 获取用户名
        if len(username) == 0: continue
        # password = input('Password: ').strip()
        password = getpass.getpass('Password: ').strip() # 获取密码
        user = dbconn.session.query(dbmodels.UserProfile).filter(dbmodels.UserProfile.username == username, dbmodels.UserProfile.password == password).first()
        if user: # 验证用户
            return user
        else:
            mylib.print_err(conf.ERRORNO['1001'])
            count += 1
    else:
        mylib.print_err(conf.ERRORNO['1002'])

def print_welcome(user):
    '''
    打印欢迎信息函数
    :param user:
    :return:
    '''
    WELCOME_MSG = conf.WELCOME_MSG
    print(mylib.color(WELCOME_MSG, 36))


def open_session(user, hostuser):
    '''
    打开会话函数
    :param user: 用户对象
    :param hostuser: 远端主机对象
    :return: 无
    '''
    from models.supertty import myTty # 导入myTty包
    # def __init__(self, user, ip, username, port, password, rsa_key = None):
    mytty = myTty(user, hostuser) # 创建myTty对象
    mytty.run() # 运行入口方法


def start(argvs):
    '''
    堡垒机主函数
    :param argvs: 命令行参数，本函数用不到
    :return: 无
    '''
    user = auth() # 调用认证函数，认证

    # user = dbconn.session.query(dbmodels.UserProfile).filter(dbmodels.UserProfile.username == 'zhangxiaoyu', dbmodels.UserProfile.password == '123.com').first()
    if user: # 认证成功执行
        flag = True
        hostusers = user.hostusers # 获取为分组的远端主机用户
        groups = user.groups # 获取组列表
        while flag:
            try:
                print_welcome(user)
                print(mylib.color('Ungrouped hosts: (%s)', 35) %len(hostusers))
                for index, hostuser in enumerate(hostusers, 1): # 遍历打印未分组远端主机用户信息
                    print('   %s.\t %s@%s(%s)' %(index, hostuser.username, hostuser.host.hostname, hostuser.host.ip_addr))
                print(mylib.color('Groups: (%s)', 35) %len(groups))
                for index, group in enumerate(groups, len(hostusers) + 1): # 遍历打印组列表
                    print('   %s.\t %s' %(index, group.name))
                chose = input('%s (q)quit>> ' %user.username) # 获取用户输入
                if chose == 'q':
                    flag = False
                elif chose.isdigit():
                    chose = int(chose)
                    if 0 < chose < len(hostusers) + 1: # 判断是否在未分组主机列表中
                        hostuser = hostusers[chose - 1] # 获取远端主机信息
                        open_session(user, hostuser) # 打开会话
                    elif len(hostusers) < chose < (len(hostusers) + len(groups) + 1): # 否则选择的就是组
                        group = groups[chose - len(hostusers) -1] # 获取组
                        group_flag = True
                        while group_flag:
                            for index, hostuser in enumerate(group.host_users, 1): # 遍历打印当前组内的远端主机列表
                                print('   %s.\t %s@%s(%s)' %(index, hostuser.username, hostuser.host.hostname, hostuser.host.ip_addr))
                            chose2 = input('zhangxiaoyu (q)quit, (b)break>> ').strip()
                            if chose2.isdigit():
                                chose2 = int(chose2)
                                if 0 < chose2 < (len(group.host_users) + 1): # 判断是否在远端主机用户列表中
                                    hostuser = group.host_users[chose2 - 1]
                                    open_session(user, hostuser) # 打开会话
                                    group_flag = False
                                else:
                                    mylib.print_err(conf.ERRORNO['2002'])
                            elif chose2 == 'q':
                                group_flag = False
                                flag = False
                            elif chose2 == 'b':
                                group_flag = False
                            else:
                                mylib.print_err(conf.ERRORNO['2002'])
                    else:
                        mylib.print_err(conf.ERRORNO['2002'])
                else:
                    mylib.print_err(conf.ERRORNO['2002'])
            except (EOFError,BlockingIOError) as e:
                continue
                exit(1)


def stop():
    '''
    结束函数，预留
    :return:
    '''
    pass

def import_hosts(argvs):
    '''
    导入主机列表函数
    :param argvs: 命令行参数列表
    :return: 无
    '''
    import os
    import json
    if '-f' in argvs: # 判断参数列表是否合法
        hosts_file = argvs[argvs.index("-f") + 1] # 获取主机列表文件
    else:
        mylib.print_err(conf.ERRORNO['3001'] %"import_host -f [/path/to/file]", quit = True)
    if os.path.isfile(hosts_file): # 判断文件是否存在
        f = open(hosts_file, 'r')
        host_list = json.load(f) # 解析文件
        # print(host_list)
        for host in host_list: # 遍历列表
            # 插入数据
            host_obj = dbmodels.Host(hostname = host.get('hostname'), ip_addr = host.get('ip_addr'), port = host.get('port') or 22)
            dbconn.session.add(host_obj)
        dbconn.session.commit()
        f.close()
    else:
        mylib.print_err(conf.ERRORNO['4001'] %hosts_file, quit = True)

def import_remoteusers(argvs):
    '''
    导入远端用户方法
    :param argvs: 命令行参数
    :return:
    '''
    import os
    import json
    if '-f' in argvs:
        remotusers_file = argvs[argvs.index("-f") + 1]
    else:
        mylib.print_err(conf.ERRORNO['3001'] %"import_remoteuser -f [/path/to/file]", quit = True)
    if os.path.isfile(remotusers_file):
        f = open(remotusers_file, 'r')
        user_list = json.load(f)
        for user in user_list: # 便利远端主机用户
            hostname = user.get('hostname')
            # 获取主机
            host_obj = dbconn.session.query(dbmodels.Host).filter(dbmodels.Host.hostname == hostname).first()
            # 创建用户对象
            user_obj = dbmodels.HostUser(username = user.get('username'), password = user.get('password'), auth_type = user.get('auth_type'), host = host_obj)
            # 插入数据
            dbconn.session.add(user_obj)
        dbconn.session.commit()
        f.close()
    else:
        mylib.print_err(conf.ERRORNO['4001'] %hosts_file, quit = True)

def import_groups(argvs):
    '''
    导入分组函数（注意这里的分组指的是远端主机用户的分组）
    :param argvs: 命令行参数
    :return: 无
    '''
    import os
    import json
    if '-f' in argvs:
        groups_file = argvs[argvs.index("-f") + 1]
    else:
        mylib.print_err(conf.ERRORNO['3001'] %"import_remoteuser -f [/path/to/file]", quit = True)
    if os.path.isfile(groups_file):
        f = open(groups_file, 'r')
        group_list = json.load(f)
        for group in group_list: # 遍历组列表
            groupname = group.get('name')
            hostusers = group.get('hostusers')
            group = dbmodels.Group(name = groupname) # 创建组对象
            for hostuser in hostusers: # 遍历远端主机列表
                # 获取主机
                host = dbconn.session.query(dbmodels.Host).filter(dbmodels.Host.hostname == hostuser.get('hostname')).first()
                # 获取远端主机对象
                hostuser_obj = dbconn.session.query(dbmodels.HostUser).filter(dbmodels.HostUser.username == hostuser.get('username'), dbmodels.HostUser.host == host).first()
                # 添加主机用户到组
                group.host_users.append(hostuser_obj)
            # 插入数据
            dbconn.session.add(group)
        dbconn.session.commit()
        f.close()
    else:
        mylib.print_err(conf.ERRORNO['4001'] %groups_file, quit = True)

def import_users(argvs):
    '''
    导入用户列表（这里的用户指的是堡垒机的用户）
    :param argvs: 命令行参数
    :return:
    '''
    import os
    import json
    if '-f' in argvs:
        users_file = argvs[argvs.index("-f") + 1]
    else:
        mylib.print_err(conf.ERRORNO['3001'] %"import_users -f [/path/to/file]", quit = True)
    if os.path.isfile(users_file):
        f = open(users_file, 'r')
        user_list = json.load(f)
        for user in user_list: # 遍历用户列表
            username = user.get('username')
            password = user.get('password')
            hostusers = user.get('hostusers')
            user_obj = dbmodels.UserProfile(username = username, password = password) # 创建用户对象
            for hostuser in hostusers: # 遍历未分组远端主机用户
                # 获取主机对象
                host = dbconn.session.query(dbmodels.Host).filter(dbmodels.Host.hostname == hostuser.get('hostname')).first()
                # 获取远端用户对象
                hostuser_obj = dbconn.session.query(dbmodels.HostUser).filter(dbmodels.HostUser.username == hostuser.get('username'), dbmodels.HostUser.host == host).first()
                # 追加未分组远端主机用户
                user_obj.hostusers.append(hostuser_obj)
            # 获取组列表
            groups = dbconn.session.query(dbmodels.Group).filter(dbmodels.Group.name.in_(user.get('groups'))).all()
            user_obj.groups = groups # 组列表等于获取的列表
            # 插入数据
            dbconn.session.add(user_obj)
        dbconn.session.commit()
        f.close()
    else:
        mylib.print_err(conf.ERRORNO['4001'] %users_file, quit = True)

def init_database(argvs):
    print("Init database...")
    dbmodels.Base.metadata.create_all(dbconn.engine)