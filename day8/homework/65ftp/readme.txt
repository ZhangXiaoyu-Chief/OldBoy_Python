#################################################
# Created on: 2016年3月11日
# @author: 张晓宇
# Email: 61411916@qq.com
# Blog: http://www.cnblogs.com/zhangxiaxuan/
# GitHub: https://github.com/ZhangXiaoyu-Chief
#################################################


作业一：继续完善ftp服务器

本此作业版本与上次版本做出的改进：
1、优化了代码
2、修改了rm、cd命令的目录算法，尤其是修改了目录是否合法的算法，使命令更符合原生linux使用习惯
3、修改了家目录已使用大小的算法，使用原生du -s获取已经使用的大小
4、修复了上传的bug
5、服务端和客户端分离，成为两个独立的目录，并使用不通的配置文件
6、使用错误码列表的方式统一了报错信息
7、服务端增加日志输出
8、取消了pwd命令，当前目录直接显示在命令提示符上
9、get命令增加了可以保存到其他目录的功能

程序结构：
.
├── ftpclient # 客户端目录
│   ├── conf # 配置文件目录
│   │   ├── conf.py # 客户端配置文件
│   │   └── __init__.py
│   ├── ftp_client.py # 客户端主程序
│   ├── libs # 自定义库目录
│   │   ├── __init__.py
│   │   ├── mylib.py
│   │   └── progressbar.py
│   └── model # 模型目录
│       ├── client.py
│       └── __init__.py
└── ftpserver # 服务端目录
    ├── conf
    │   ├── conf.py # 客户端配置文件
    │   └── __init__.py
    ├── dbs # 数据目录
    │   └── users.db # 用户数据
    ├── ftp_server.py # 服务端主程序
    ├── home 用户家目录
    │   ├── guest
    │   │   └── test
    │   └── zhangxiaoyu
    │       └── test
    ├── libs # 自定义库文件
    │   ├── __init__.py
    │   ├── mylib.py
    │   └── progressbar.py
    ├── logs # 日志目录
    │   └── 65ftp_server.log
    └── model # 模型目录
        ├── __init__.py
        ├── server.py
        └── users.py



程序配置：
服务端配置文件：
import os
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 基础目录
HOME_PATH = '%s/home' %BASE_DIR # 用户家目录
CODE_LIST = { # 错误列表
    '200': "Pass authentication!",
    '201': "Authentication fail wrong username or password",
    '300': "Ready to send file to client",
    '301': "Client ready to receive file data ",
    '302': "File doesn't exist",
    '303': "Path doesn't exist",
    '304': "Destination path doesn't exist",
    '305': "IO error",
    '306': "Socket error",
    '307': "Insufficient space",
    "308": "Validate successful",
    "309": "Validate fail",
    "310": "Path or file doesn't exixt",
    '401': "Invalid instruction!",
    '500': "Invalid execute successful",
    '501': "Invalid execute fail",
}
SERVER_IP = '0.0.0.0' # 监听IP地址
PORT = 9998 # 监听端口
USER_FILE = 'dbs/users.db' # 用户文件地址
LOGS = 'logs/65ftp_server.log' # 日志文件
DEFAULT_QUOTA = 500 # 默认目录配额，单位MB
FILE_PER_SIZE = 1024 # 每次数据传输的大小，单位字节

客户端配置文件：
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOME_PATH = '%s/home' %BASE_DIR

TMP_PATH = '%s/tmp' %BASE_DIR

CODE_LIST = {
    '200': "Pass authentication!",
    '201': "Authentication fail wrong username or password",
    '300': "Ready to send file to client",
    '301': "Client ready to receive file data ",
    '302': "File doesn't exist",
    '303': "Path doesn't exixt",
    '304': "Destination path doesn't exist",
    '305': "IO error",
    '306': "Socket error",
    '307': "Insufficient space",
    "308": "Validate successful",
    "309": "Validate fail",
    "310": "Path or file doesn't exixt",
    '401': "Invalid instruction!",
    '500': "Invalid execute successful",
    '501': "Invalid execute fail",
}

SERVER_IP = '127.0.0.1' # 服务端IP地址

FILE_PER_SIZE = 1024

PORT = 9998 # 服务端端口

USER_FILE = 'dbs/user.db'

LOGS = 'logs/65ftp_server.log'

DEFAULT_QUOTA = 500

数据文件：
    {
        "username" : "zhangxiaoyu", # 用户名
        "password" : "cbff36039c3d0212b3e34c23dcde1456", # 密码
        "home" : "home/zhangxiaoyu/", # 家目录
        "quota" : 500 # 配额
    }


运行环境：暂不支持windows主机，Python3.0或以上版本并配置好环境变量（linux主机为了和自带的python2.x版本不冲突，需将python3.X的可执行文件重名为python3或创建名为python3的软链接链接到python的可执行文件）

执行方法：
    服务端
        1、Linux：直接执行# python3 ftp_server.py或#./ftp_server.py（需要给主程序文件添加可执行权限）
    客户端
        1、Linux：直接执行# python3 ftp_client.py或#./ftp_client.py（需要给主程序文件添加可执行权限）


使用方法：
     服务端启动后就不用管了，主要是客户端操作
     get:  用于下载文件，格式：get path/to/filename，说明：path/to/格式要求同cd命令
         guest: >> get QQ_8.1.17255.0_setup.1456298445.exe
         100.00  [##################################################] 56,275,304
         Validating...
     auth:  用户认证，格式：auth，然后根据提示输入用户名及密码
        guest >> auth
        username: zhangxiaoyu
        password: 123.com
        Pass authentication!
        zhangxiaoyu: >>
     cd:  用于下载文件，格式：get path/to/filename [dst/path/to/]，说明：path/to/格式要求同cd命令, dst/path/to/为目标目录，暂时只能使用相对目录
        zhangxiaoyu: >> cd test
        zhangxiaoyu:test/ >>
     ls:  用于显示当前目录下文件或文件详细信息，格式：ls
        zhangxiaoyu:test >> ls
        total 8
        drwxr-xr-x 2 root root 4096 Mar  4 10:44 .
        drwxr-xr-x 3 root root 4096 Mar  4 10:44 ..
     put:  用于上传文件，格式：put path/to/filename，说明：path/to/格式要求同cd命令
        guest >> put QQ_8.1.17255.0_setup.1456298445.exe
        100.00  [##################################################] 56,275,304
     rm:  用于删除文件或目录，格式：rm path/to[/filename]，说明：path/to/格式要求同cd命令
        guest >> rm qq.exe