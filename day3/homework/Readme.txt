#################################################
# Created on: 2016年1月21日
# @author: 张晓宇
# Email: 61411916@qq.com
# Blog: http://www.cnblogs.com/zhangxiaxuan/
# GitHub: https://github.com/ZhangXiaoyu-Chief
#################################################


作业一：修改Haproxy配置文件
    1、获取ha记录通过用户输入的backend名称显示该backend下所有记录
    2、新增或修改ha记录，用户输入类似：{"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}，分为如下3种情况
       1）如果backend存在查看是否有ip地址相同的记录，如果没有则添加没。
       2）如果有ip地址相同的记录，则修改ha记录。
       3）如果backend不存在则新建backend，并添加记录
    3、删除，用户输入类似{"backend": "test.oldboy.org","record":{"server": "100.1.7.9"}}删除对应的记录，如果一个backend的记录已经为空了，删除backend

程序结构：
.
├── conf.py #=> 程序配置文件
├── haproxy.conf #=> haproxy配置文件
├── model #=> 模型模块
│   ├── haproxy.py #=> haproxy模块
│   └── __init__.py
├── Readme.txt
├── haproxy_configuration.py #=> 主程序
└── utility #=> 功能模块
    ├── __init__.py
    └── MyFileHelper.py #=> 文件操作模块

程序配置：
    配置文件：conf.py
        main_menu = ['获取Haproxy记录', '增加/修改Haproxy记录', '删除Haproxy记录', '将修改写入到文件', '显示全部backend'] # 主菜单选项
        haproxy_file = "haproxy.conf" # haproxy配置文件
        indentation = 4 # backend下record的缩进
        record_op_list = ['server','weight', 'maxconn'] # backend记录里的合法字段名
        record_op = {'server':"", 'weight':0 , 'maxconn':0} # backend记录里的合法字段名所对应的数据类型
        conf_model # 已经废弃的想法，本来是想顶一个配置文件模板，定义不同的节点的位置，然后通过字符串的format方法组装配置文件


运行环境：Python3.0或以上版本并配置好环境变量（linux主机为了和自带的python2.x版本不冲突，需将python3.X的可执行文件重名为python3或创建名为python3的软链接链接到python的可知文件）

执行方法：
    1、Linux：直接执行# python3 haproxy_configuration.py或#./haproxy_configuration.py（需要给主程序文件添加可执行权限）
    2、Window：执行python haproxy_configuration.py

使用方法：
    1、主界面：输出菜单，用户通过输入相应菜单进入对应功能界面：分别为：1、获取Haproxy记录；2、增加/修改Haproxy记录；3、删除Haproxy记录；4、将修改写入到文件；5、显示全部backend
    2、获取Haproxy记录：通过输入backend名获取backend下所有record信息
    3、增加/修改Haproxy记录：用户输入类似{"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}的json字符串进行对应的增加和修改操作
       1）如果backend存在查看是否有ip地址相同的记录，如果没有则添加没。
       2）如果有ip地址相同的记录，则修改ha记录。
       3）如果backend不存在则新建backend，并添加记录
    4、删除Haproxy记录：用户输入类似{"backend": "test.oldboy.org","record":{"server": "100.1.7.9"}}的json字符串，删除对应backend下的对应record
    5、将修改写入到文件：通过用户输入确认，将当前所有修改保存到文件
    6、显示全部backend：显示所有backend的所有record


所有流程大致如下：
D:\tools\Python35\python.exe D:/OldBoy_Python_git/OldBoy_Python/day3/homework/haproxy_configuration.py

+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）              |
+-----------------------------------+
------------------------------
1、获取Haproxy记录
2、增加/修改Haproxy记录
3、删除Haproxy记录
4、将修改写入到文件
5、显示全部backend
------------------------------
请输入操作编号（输入q退出系统）：1
请输入backend（r返回上级菜单）：www.oldboy.org #===========》 输入backend名称，显示该backend下对应的记录
    server 100.1.7.9 100.1.7.9 weight 20 maxconn 3000
    server 100.1.7.8 100.1.7.8 weight 21 maxconn 3001
输入任意键继续
请输入backend（r返回上级菜单）：r

+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）              |
+-----------------------------------+
------------------------------
1、获取Haproxy记录
2、增加/修改Haproxy记录
3、删除Haproxy记录
4、将修改写入到文件
5、显示全部backend
------------------------------
请输入操作编号（输入q退出系统）：2
请输入要新加的记录（r返回上级菜单）：{"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}} #===========》 用户输入合法的json字符串，如果不合法，报出对应错误
添加成功，按任意键继续 #===========》通过合法验证新增记录
请输入要新加的记录（r返回上级菜单）：r

+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）              |
+-----------------------------------+
------------------------------
1、获取Haproxy记录
2、增加/修改Haproxy记录
3、删除Haproxy记录
4、将修改写入到文件
5、显示全部backend
------------------------------
请输入操作编号（输入q退出系统）：1
请输入backend（r返回上级菜单）：test.oldboy.org #===========》 验证新增
    server 100.1.7.9 100.1.7.9 weight 20 maxconn 30
输入任意键继续
请输入backend（r返回上级菜单）：r

+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）              |
+-----------------------------------+
------------------------------
1、获取Haproxy记录
2、增加/修改Haproxy记录
3、删除Haproxy记录
4、将修改写入到文件
5、显示全部backend
------------------------------
请输入操作编号（输入q退出系统）：2
请输入要新加的记录（r返回上级菜单）：{"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 300}} #===========》 这里100.1.7.9之前已经添加，我们修改"maxconn"的值由30改为300
添加成功，按任意键继续
请输入要新加的记录（r返回上级菜单）：r

+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）              |
+-----------------------------------+
------------------------------
1、获取Haproxy记录
2、增加/修改Haproxy记录
3、删除Haproxy记录
4、将修改写入到文件
5、显示全部backend
------------------------------
请输入操作编号（输入q退出系统）：1
请输入backend（r返回上级菜单）：test.oldboy.org #===========》 验证修改
    server 100.1.7.9 100.1.7.9 weight 20 maxconn 300 #===========》 成功修改
输入任意键继续
请输入backend（r返回上级菜单）：r

+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）              |
+-----------------------------------+
------------------------------
1、获取Haproxy记录
2、增加/修改Haproxy记录
3、删除Haproxy记录
4、将修改写入到文件
5、显示全部backend
------------------------------
请输入操作编号（输入q退出系统）：5 #===========》 显示所有backend的多有record
backend www.oldboy.org
    server 100.1.7.9 100.1.7.9 weight 20 maxconn 3000
    server 100.1.7.8 100.1.7.8 weight 21 maxconn 3001
backend buy.oldboy.org
    server 100.1.7.90 100.1.7.90 weight 20 maxconn 3000
backend test.oldboy.org
    server 100.1.7.9 100.1.7.9 weight 20 maxconn 300

按任意键继续

+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）              |
+-----------------------------------+
------------------------------
1、获取Haproxy记录
2、增加/修改Haproxy记录
3、删除Haproxy记录
4、将修改写入到文件
5、显示全部backend
------------------------------
请输入操作编号（输入q退出系统）：3
请输入要新加的记录（r返回上级菜单）：{"backend": "buy.oldboy.org","record":{"server": "100.1.7.90"}} #===========》 删除
删除成功，按任意键继续
请输入要新加的记录（r返回上级菜单）：r

+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）              |
+-----------------------------------+
------------------------------
1、获取Haproxy记录
2、增加/修改Haproxy记录
3、删除Haproxy记录
4、将修改写入到文件
5、显示全部backend
------------------------------
请输入操作编号（输入q退出系统）：5 #===========》 显示所有backend的多有record，验证是否删除
backend www.oldboy.org
    server 100.1.7.9 100.1.7.9 weight 20 maxconn 3000
    server 100.1.7.8 100.1.7.8 weight 21 maxconn 3001
backend test.oldboy.org
    server 100.1.7.9 100.1.7.9 weight 20 maxconn 300

按任意键继续

+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）              |
+-----------------------------------+
------------------------------
1、获取Haproxy记录
2、增加/修改Haproxy记录
3、删除Haproxy记录
4、将修改写入到文件
5、显示全部backend
------------------------------
请输入操作编号（输入q退出系统）：4 #===========》 写入到文件
确认是否将修改写入到配置文件中（y）: y
写入文件成功，按任意键继续

+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）              |
+-----------------------------------+
------------------------------
1、获取Haproxy记录
2、增加/修改Haproxy记录
3、删除Haproxy记录
4、将修改写入到文件
5、显示全部backend
------------------------------
请输入操作编号（输入q退出系统）：q #===========》 退出系统