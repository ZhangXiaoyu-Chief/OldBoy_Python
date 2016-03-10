├── 65bhms.py
├── conf
│   ├── conf.py
│   └── __init__.py
├── libs
│   ├── __init__.py
│   ├── mylib.py
│   └── progressbar.py
├── logs
│   └── manager.log
├── model
│   ├── __init__.py
│   └── manager.py
└── rsas
    └── id_rsa


.
├── ftpclient
│   ├── bin
│   │   └── __init__.py
│   ├── conf
│   │   ├── conf.py
│   │   └── __init__.py
│   ├── dbs
│   │   └── users.db
│   ├── ftp_client.py
│   ├── libs
│   │   ├── __init__.py
│   │   ├── mylib.py
│   │   └── progressbar.py
│   └── model
│       ├── client.py
│       ├── __init__.py
│       └── users.py
└── ftpserver
    ├── bin
    │   └── __init__.py
    ├── conf
    │   ├── conf.py
    │   └── __init__.py
    ├── dbs
    │   └── users.db
    ├── ftp_server.py
    ├── libs
    │   ├── __init__.py
    │   ├── mylib.py
    │   └── progressbar.py
    └── model
        ├── __init__.py
        ├── server.py
        └── users.py

get:  用于下载文件，格式：get path/to/filename [dst/path/to/]，说明：path/to/格式要求同cd命令, dst/path/to/为目标目录，暂时只能使用相对目录
      cd:  用于切换服务端目录，格式：cd path/to/，说明只能使用相对目录，‘.’表示当前目录，‘..’表示父目录
     put:  用于上传文件，格式：put path/to/filename，说明：path/to/格式要求同cd命令
    auth:  用户认证，格式：auth，然后根据提示输入用户名及密码
      rm:  用于删除文件或目录，格式：rm path/to[/filename]，说明：path/to/格式要求同cd命令
      ls:  用于显示当前目录下文件或文件详细信息，格式：ls