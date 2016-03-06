#################################################
# Created on: 2016年3月3日
# @author: 张晓宇
# Email: 61411916@qq.com
# Blog: http://www.cnblogs.com/zhangxiaxuan/
# GitHub: https://github.com/ZhangXiaoyu-Chief
#################################################


作业一：ftp服务器

程序结构：
.
├── conf
│   ├── conf.py # 配置文件
│   └── __init__.py
├── core
│   ├── core.py # 主逻辑文件
│   ├── __init__.py
├── dbs
│   └── users.db # 用户数据文件
├── ftp_client.py # 客户端
├── ftp_server.py # 服务端
├── home # 用户家目录
│   ├── tmp
│   └── zhangxiaoyu
├── libs
│   ├── __init__.py
│   └── mylib.py
└── model # 模块目录
    ├── client.py # 客户端模块
    ├── __init__.py
    ├── server.py # 服务端模块
    └── users.py # 用户模块



程序配置：
    配置文件conf.py
    IP_PORT = ('127.0.0.1',9999) # ftp的监听IP和端口

    USERS_FILE = 'dbs/users.db' # 用户数据文件

    FILE_PER_SIZE = 1024 # 每次传输的数据大小，单位字节

    TMP_SPACE_SIZE = 1024 * 1024 * 1024 # 匿名用户家目录容量

    JINDO_MAX = 40 # 进度条宽度

数据文件：
    {
        "username" : "zhangxiaoyu", # 用户名
        "password" : "cbff36039c3d0212b3e34c23dcde1456", # 密码
        "home" : "home/zhangxiaoyu/", # 家目录
        "status" : "正常",
        "error_count" : 0,
        "max_size" : 1073741824 # 家目录容量
    }


运行环境：暂不支持windows主机，Python3.0或以上版本并配置好环境变量（linux主机为了和自带的python2.x版本不冲突，需将python3.X的可执行文件重名为python3或创建名为python3的软链接链接到python的可知文件）

执行方法：
    服务端
        1、Linux：直接执行# python3 ftp_server.py或#./ftp_server.py（需要给主程序文件添加可执行权限）
    客户端
        1、Linux：直接执行# python3 ftp_client.py或#./ftp_client.py（需要给主程序文件添加可执行权限）


使用方法：
    服务端启动后就不用管了，主要是客户端操作
     get:  用于下载文件，格式：get path/to/filename，说明：path/to/格式要求同cd命令
         guest >> get QQ_8.1.17255.0_setup.1456298445.exe
         100.00  [##################################################] 56,275,304
         正在验证下载的文件...
         文件验证成功...
         文件下载成功
    auth:  用户认证，格式：auth，然后根据提示输入用户名及密码
        guest >> auth
        username: zhangxiaoyu
        password: 123.com
        ok
        zhangxiaoyu >>
     pwd:  用于显示当前目录，格式：pwd
        zhangxiaoyu >> pwd
        home/zhangxiaoyu/
      cd:  用于切换服务端目录，格式：cd path/to/，说明~或/表示用户家目录，但是不能/path/to/或 ~/path/to/，‘.’表示当前目录，‘..’表示父目录
        zhangxiaoyu >> cd test
        ok
        zhangxiaoyu >> pwd
        home/zhangxiaoyu/test/
      ls:  用于显示当前目录下文件或文件详细信息，格式：ls
        zhangxiaoyu >> ls
        total 8
        drwxr-xr-x 2 root root 4096 Mar  4 10:44 .
        drwxr-xr-x 3 root root 4096 Mar  4 10:44 ..
     put:  用于上传文件，格式：put path/to/filename，说明：path/to/格式要求同cd命令
        guest >> rm QQ_8.1.17255.0_setup.1456298445.exe
        ok
        guest >> put QQ_8.1.17255.0_setup.1456298445.exe
        can
        ########################################
        上传成功
    move:  用于移动或重命名文件，格式：move path/to[/old_filename] move path/to[/new_filename]，说明：path/to/格式要求同cd命令
        guest >> move QQ_8.1.17255.0_setup.1456298445.exe qq.exe
        ok
        guest >> ls
        total 54972
        drwxr-xr-x 2 root root     4096 Mar  4 10:50 .
        drwxr-xr-x 4 root root     4096 Mar  4 10:02 ..
        -rw-r--r-- 1 root root 56275304 Mar  4 10:19 qq.exe
      rm:  用于删除文件或目录，格式：rm path/to[/filename]，说明：path/to/格式要求同cd命令
        guest >> rm qq.exe
        ok
        guest >> ls
        total 8
        drwxr-xr-x 2 root root 4096 Mar  4 10:51 .
        drwxr-xr-x 4 root root 4096 Mar  4 10:02 ..


