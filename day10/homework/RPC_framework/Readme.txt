#################################################
# Created on: 2016年3月25日
# @author: 张晓宇
# Email: 61411916@qq.com
# Blog: http://www.cnblogs.com/zhangxiaxuan/
# GitHub: https://github.com/ZhangXiaoyu-Chief
#################################################

作业二、RabbitMQ RPC远端执行命令

程序结构：
.
├── conf                    # 配置文件目录
│   ├── conf.py             # 主配置文件
│   └──  __init__.py
├── libs                    # 公共库目录
│   ├── __init__.py
│   ├── mylib.py
│   └──  progressbar.py
├── logs                    # 日志目录
│   ├── agent.log           # Agent端日志
│   └── client.log          # Client端日志
├── model                   # 模型目录
│   ├── __init__.py
│   ├── rpcAgent.py         # Agent端模型
│   └── rpcClient.py        # Client端模型
├── rpcAgent.py             # Agent端主程序
└── rpcClient.py            # Client端主程序

程序配置：
配置文件conf.py：
    #!/usr/bin/env python3
    # coding:utf-8
    RBMQ_HOST = '10.10.1.133'       # RabbitMQ服务器地址
    QUEUE = 'rpc_que'               # 队列名称
    EXCHANGE = 'rpc_ex'             # exchange名称
    TIME_OUT = 5                    # 超时时间，广播命令并接收返回结果，如果收到如果超时间内没有收到，将会被丢弃

    AGENT_NAME = 'web1'             # agent端主机名，用来区分不同主机返回的结果
    CLIENT_LOG = 'logs/client.log'  # client端日志文件
    AGENT_LOG = 'logs/agent.log'    # agent端日志文件


运行环境：
    1、暂不支持windows主机，Python3.0或以上版本并配置好环境变量（linux主机为了和自带的python2.x版本不冲突，需将python3.X的可执行文件重名为python3或创建名为python3的软链接链接到python的可执行文件）
    2、需要安装第三方的pika库，具体安装方法，自己百度
    3、需要一台部署好的RabbitMQ服务器，用于提供消息服务

执行方法：进入程序目录后按照如下方法启动
    1、Linux：
        1)Agent端（执行命令端）：直接执行# python3 cpcAgent.py 或#./cpcAgent（需要给主程序文件添加可执行权限）
        2)Client端（发送命令端）：直接执行# python3 cpcClient.py [commend]或#./cpcClient.py（需要给主程序文件添加可执行权限）
    2、Windows：暂不支持Windows
        1)Agent端：直接执行# python3 cpcAgent.py
        2)Client端：直接执行# python cpcClient.py [commend]

使用方法：
    配置好指令文件后直接按照执行方执行即可

    D:\x学习\pythonsrc\S12_src\OldBoy_Python\day10\homework\RPC_framework>python rpcClient.py df -h
    2016-03-25 09:36:46 [INFO]: Connecting to 10.10.1.133:5672
    2016-03-25 09:36:46 [INFO]: Created channel=1
    2016-03-25 09:36:46 [INFO]: excute commend df -h
    [web1]
    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        18G  9.1G  7.6G   55% /
    none            4.0K     0  4.0K    0% /sys/fs/cgroup
    udev            987M  4.0K  987M    1% /dev
    tmpfs           200M  1.7M  198M    1% /run
    none            5.0M     0  5.0M    0% /run/lock
    none            998M  148M  850M   15% /run/shm
    none            100M   84K  100M    1% /run/user
    /dev/sda1       180M   36M  131M   22% /boot

    [web2]
    文件系统        容量  已用  可用 已用% 挂载点
    /dev/sda3        18G  9.1G  7.6G   55% /
    none            4.0K     0  4.0K    0% /sys/fs/cgroup
    udev            987M  4.0K  987M    1% /dev
    tmpfs           200M  1.7M  198M    1% /run
    none            5.0M     0  5.0M    0% /run/lock
    none            998M  148M  850M   15% /run/shm
    none            100M   84K  100M    1% /run/user
    /dev/sda1       180M   36M  131M   22% /boot

    如果命令执行失败会返回错误信息类似如下
    D:\x学习\pythonsrc\S12_src\OldBoy_Python\day10\homework\RPC_framework>pthon rpcClient.py daf
    2016-03-25 09:48:41 [INFO]: Connecting to 10.10.1.133:5672
    2016-03-25 09:48:41 [INFO]: Created channel=1
    2016-03-25 09:48:41 [INFO]: excute commend daf
    [web1]
    /bin/sh: 1: daf: not found

    [web1]
    /bin/sh: 1: daf: not found


