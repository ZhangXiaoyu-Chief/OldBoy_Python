#################################################
# Created on: 2016年3月17日
# @author: 张晓宇
# Email: 61411916@qq.com
# Blog: http://www.cnblogs.com/zhangxiaxuan/
# GitHub: https://github.com/ZhangXiaoyu-Chief
#################################################

作业二、批量主机管理工具（模仿saltstak）
版本变更历史：
较上次作业，做了如下改进
1、代码架构做了调整，通过不同模块来对主要功能（执行命令，上传下载）进行了划分
2、不再是通过命令行传参的形式执行批量操作，而是通过编写指令文件的形式执行批量操作，真正实现了自动化
3、由于调整了代码结构，并且通过反射实现执行不同模块的不同方法，易于扩展
4、优化了代码，定义了自定义错误，并结合raise关键字抛出异常的方式实现代码的精简优化


程序结构：
.
├── conf # 配置文件
│   ├── conf.py # 主配置文件
│   ├── hosts.conf # 主机列表配置文件
│   └── __init__.py
├── core
│   ├── core.py # 主逻辑
│   └── __init__.py
├── libs # 自定义库
│   ├── __init__.py
│   ├── mylib.py
│   └── progressbar.py
├── logs # 日志目录
│   └── my_saltstack.log
├── model # 模型目录
│   └── myParamiko.py # 对Paramiko的一些封装
├── module # 模块目录
│   ├── cmd.py # 执行命令模块
│   ├── file.py # 文件操作模块
│   └── __init__.py
├── my_salt.py # 主执行文件
└── sls # 指令文件
    └── webserver_run.sls # 测试用指令文件

程序配置：
配置文件conf.py：
    #!/usr/bin/env python3
    # coding:utf-8
    import os
    BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 基目录

    LOG_FILE = '%s/logs/my_saltstack.log' %BASE_DIR # 日志文件

    MULT_NUM = 5 # 进程数

    HOSTS_FILE = '%s/conf/hosts.conf' %BASE_DIR # 主机列表配置文件
主机列表配置文件：hosts.conf
    123.59.44.38: # 主机名（ip地址）
      username: ubuntu # 用户名
      port: 22 # 端口
      password: '!Jesus@smart8345' # 密码

    123.59.66.174:
      username: ubuntu
      port: 22
      password: '!Jesus@smart8345'

指令文件：
webserber: # 组名
  hosts: # 主机列表，注意这里出现的主机必须在主机列表文件里进行配置
    - 123.59.44.38
    - 123.59.66.174
  actions: # 指令集
      - cmd.run: # 指令，格式为模块名.函数名，这个是执行linux命令的指令
         command: 'df -h' # 指令相关的参数command表示要执行的linux命令
      - file.get: # 下载文件执行令
         src: /etc/hosts # 要下载的远程文件名，注意要使用绝对路径，并且是文件名，目前只支持单个文件下载
         dst: . # 保存下载文件的本地目录，注意是目录不是文件名
      - file.put: # 上传文件指令
         src: /home/zhangxiaoyu/PycharmProjects/OldBoy_Python/day9/shengxiao1.py # 本地文件，目前只支持单个文件上传
         dst: /home/ubuntu/ # 远端主机的目标目录


运行环境：
    1、暂不支持windows主机，Python3.0或以上版本并配置好环境变量（linux主机为了和自带的python2.x版本不冲突，需将python3.X的可执行文件重名为python3或创建名为python3的软链接链接到python的可执行文件）
    2、需要安装第三方的pramiko、yaml库，具体安装方法，自己百度

执行方法：
    1、Linux：直接执行# python3 my_salt.py /path/to指令文件或#./my_salt.py /path/to/指令文件（需要给主程序文件添加可执行权限）
    2、Windows：暂不支持Windows

使用方法：
    配置好指令文件后直接按照执行方执行即可（Linux：直接执行# python3 my_salt.py /path/to指令文件或#./my_salt.py /path/to/指令文件）
    执行结果类似如下
    $ python3 my_salt.py sls/webserver_run.sls
    [123.59.44.38] : [df -h]
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/vda1        20G   17G  1.9G  91% /
    none            4.0K     0  4.0K   0% /sys/fs/cgroup
    udev            3.9G  4.0K  3.9G   1% /dev
    tmpfs           799M  868K  798M   1% /run
    none            5.0M     0  5.0M   0% /run/lock
    none            3.9G     0  3.9G   0% /run/shm
    none            100M  4.0K  100M   1% /run/user
    /dev/vdb        197G   49G  139G  26% /data

    [123.59.66.174] : [df -h]
    Filesystem                   Size  Used Avail Use% Mounted on
    /dev/vda1                     20G   17G  1.7G  91% /
    none                         4.0K     0  4.0K   0% /sys/fs/cgroup
    udev                         7.9G  4.0K  7.9G   1% /dev
    tmpfs                        1.6G  972K  1.6G   1% /run
    none                         5.0M     0  5.0M   0% /run/lock
    none                         7.9G     0  7.9G   0% /run/shm
    none                         100M  4.0K  100M   1% /run/user
    /dev/vdb                     197G  111G   77G  60% /data
    10.10.78.203:/data/program2  197G   49G  139G  26% /data/program2

    [123.59.66.174] get file: [/etc/hosts]
    [123.59.44.38] get file: [/etc/hosts]
    get file /etc/hosts to ./20160313142116/123.59.44.38/hosts is successful
    get file /etc/hosts to ./20160313142116/123.59.66.174/hosts is successful
    [123.59.44.38] get file: [/home/zhangxiaoyu/PycharmProjects/OldBoy_Python/day9/shengxiao1.py]
    [123.59.66.174] get file: [/home/zhangxiaoyu/PycharmProjects/OldBoy_Python/day9/shengxiao1.py]
    put file 123.59.44.38 to [/home/zhangxiaoyu/PycharmProjects/OldBoy_Python/day9/shengxiao1.py]/home/ubuntu/shengxiao1.py is successful
    put file 123.59.66.174 to [/home/zhangxiaoyu/PycharmProjects/OldBoy_Python/day9/shengxiao1.py]/home/ubuntu/shengxiao1.py is successful