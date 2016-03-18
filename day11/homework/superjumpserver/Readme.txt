#################################################
# Created on: 2016年3月31日
# @author: 张晓宇
# Email: 61411916@qq.com
# Blog: http://www.cnblogs.com/zhangxiaxuan/
# GitHub: https://github.com/ZhangXiaoyu-Chief
#################################################

作业： 堡垒机

程序结构：
.
├── conf # 配置文件目录
│   ├── action_registers.py # 命令行参数指令执行函数注册配置文件
│   ├── conf.py  # 主配置文件
│   └── __init__.py
├── libs # 库目录
│   ├── __init__.py
│   ├── mylib.py
│   └── progressbar.py
├── logs # 日志目录，暂时未作本地日志收集，统统放入到数据库中，日后添加此功能
│   └── __init__.py
├── models # 模型（模块）目录
│   ├── auditlog.py # 日志模块
│   ├── dbconn.py # 数据库俩接模块
│   ├── dbmodels.py # 数据库模型
│   ├── __init__.py
│   ├── interactive.py #
│   └── supertty.py # 虚拟终端tty模块
├── share # 公共目录
│   └── examples # 批量导入模板文件目录
│       ├── groups.json
│       ├── hosts.json
│       ├── hostusers.json
│       └── users.json
├── superjumpserver.py # 程序主文件
└── views # 命令行参数调用函数目录
    └── views.py


程序配置：
主配置文件conf.py：
    #!/usr/bin/env python3
    # coding:utf-8
    # 欢迎信息
    WELCOME_MSG = '''------------------ Welcome [%s] login SuperJumpserver ------------------'''
    # 错误信息列表
    ERRORNO = {
        '1001' : 'Auth fail: wrong username or password',
        '1002' : 'Too many attempts',
        '2001' : 'Command [%s] is not exist!',
        '2002' : 'invalid option !',
        '3001' : 'Invalid usage, Usage(s): %s',
        '4001' : 'File %s is not exist!',
        '5001' : 'Connect fail!',
    }
    # 数据库连接字典
    DBS = {"test" : "mysql+pymysql://root:123.com@localhost:3306/superjumpserver_test", # 测试环境数据库
           "real" : "mysql+pymysql://root:123.com@localhost:3306/superjumpserver_test", # 正式环境数据库
           }
    # 根据实际需要切换数据库
    DB = DBS['test']


运行环境：
    1、暂不支持windows主机，Python3.0或以上版本并配置好环境变量（linux主机为了和自带的python2.x版本不冲突，需将python3.X的可执行文件重名为python3或创建名为python3的软链接链接到python的可执行文件）
    2、需要安装第三方的paramiko、sqlalchemy、sqlalchemy_util库，具体安装方法，自己百度
    3、sqlalchemy支持的数据库MySQL等（本实例为MySQL）

执行方法：进入程序目录后按照如下方法启动
    1、Linux：直接执行# python3 superjumpserver.py [commend [otpions]] 或#./superjumpserver.py[commend [otpions]]（需要给主程序文件添加可执行权限）
    2、Windows：暂不支持Windows

使用方法：
    初始化配置：用于第一次运行堡垒机程序，创建数据库、数据库表批量导入数据
        1、创建数据库、数据库用户，以MySQL为例
            mysql> create database superjumpserver_test charset=utf8;

            mysql> grant all on superjumpser_test.* to superjumpser@'%' identified by '123.com';
            Query OK, 0 rows affected (0.03 sec)

            mysql> flush privileges;
            Query OK, 0 rows affected (0.02 sec)
        2、配置数据库链接，修改主配置文件DBS和DB字段
        3、初始化数据库表
            $ python3 superjumpserver.py init_database
            Init database...
        4、导入主机列表
        1）准备主机列表文件(json格式)，例如
            [
              {
                "hostname" : "web1", # 主机名，要求必须唯一
                "ip_addr" : "192.168.0.250", # IP地址，要求必须唯一
                "port" : 22 # 端口
              },
              {
                "hostname" : "mysql",
                "ip_addr" : "192.168.0.251",
                "port" : 22
              },
              {
                "hostname" : "test",
                "ip_addr" : "127.0.0.1"
              }
            ]
        2）批量导入，（通过-f选项制定文件目录）
            $ python3 superjumpserver.py import_hosts -f share/examples/hosts.json
        5、导入远端主机用户列表
        1）准备远端主机用户列表(json格式)，例如
            [
              {
                "username" : "root", # 用户名
                "password" : "123456", # 密码（ssh-key认证方式可省略）
                "hostname" : "web1", # 主机名，与主机列表的主机必须一致
                "auth_type" : "ssh-password" # 认证类型：ssh-password（密码）/ssh-key（密钥）
              },
              {
                "username" : "root",
                "hostname" : "mysql",
                "auth_type" : "ssh-key"
              },
              {
                "username" : "root",
                "password" : "123456",
                "hostname" : "test",
                "auth_type" : "ssh-key"
              },
              {
                "username" : "zhangxiaoyu",
                "password" : "123.com",
                "hostname" : "test",
                "auth_type" : "ssh-password"
              }
            ]
        2）批量导入，（通过-f选项制定文件目录）
            $ python3 superjumpserver.py import_remoteusers -f share/examples/hostusers.json
        6、导入远端主机用户组列表（注意，是远端用户的组不是主机的组）
        1）准备远端主机用户组列表(json格式)，例如
            [
              {
                "name" : "webgroup", # 组名，要求必须唯一
                "hostusers" : [
                                {
                                  "username":"root", # 用户名
                                  "hostname":"web1"}, # 主机名，必须与主机表的主机名一致
                                {
                                  "username":"zhangxiaoyu",
                                  "hostname":"test"}
                                ] # 远端用户列表
              },
              {
                "name" : "dbgroup",
                "hostusers" : [{"username":"root", "hostname":"mysql"}]
              }
            ]
        2）批量导入，（通过-f选项制定文件目录）
            $ python3 superjumpserver.py import_groups -f share/examples/groups.json
        7、导入堡垒机用户列表（注意，是堡垒机用户）
        1）准备远端主机用户组列表(json格式)，例如
            [
              {
                "username" : "zhangxiaoyu", # 用户名
                "password" : "123.com", # 密码
                "hostusers" : [{"username":"root", "hostname":"mysql"}], # 未分组的远端主机用户列表，格式和组类似
                "groups" : ["webgroup"] # 组列表，这里只是组名，要求和组一致
              }
            ]
        2）批量导入，（通过-f选项制定文件目录）
            $ python3 superjumpserver.py import_users -f share/examples/users.json
        至此，初始化配置工作就完成了，下面就让我们畅快的使用吧
    使用：
        1、启动并登录进入主界面
        $ python3 superjumpserver.py start
        Username: zhangxiaoyu
        Password:
        ------------------ Welcome [%s] login SuperJumpserver ------------------
        Ungrouped hosts: (1)
           1.	 root@mysql(192.168.0.251)
        Groups: (1)
           2.	 webgroup
        2、在主界面只需要菜单编号进行选择就可以了，可以直接选择未分组的主机或选择组在通过组下面的远程用户登录远程主机
        ------------------ Welcome [%s] login SuperJumpserver ------------------
        Ungrouped hosts: (1)
           1.	 root@mysql(192.168.0.251)
        Groups: (1)
           2.	 webgroup
        zhangxiaoyu (q)quit>> 2
           1.	 root@web1(192.168.0.250)
           2.	 zhangxiaoyu@test(127.0.0.1)
        zhangxiaoyu (q)quit, (b)break>> 2
        Connect remote host [127.0.0.1] as user [zhangxiaoyu]...
        Connect success let's go [zhangxiaoyu]
        Welcome to Ubuntu 14.04.2 LTS (GNU/Linux 3.16.0-30-generic x86_64)

         * Documentation:  https://help.ubuntu.com/

        359 packages can be updated.
        190 updates are security updates.

        Last login: Fri Mar 18 08:37:55 2016 from 10.10.1.1
        zhangxiaoyu@zhangxiaoyu-python:~$
        说明：怎么样是不是很神奇，使用也非常简单，还在想什么，赶紧试试吧


