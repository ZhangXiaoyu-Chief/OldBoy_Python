#!/usr/bin/env python3
# coding:utf-8

app_info = '''
+-----------------------------------+
| Haproxy_configuration system      |
| 版本: 1.0                         |
| 作者: 张晓宇（65年哥）            |
+-----------------------------------+'''

main_menu = ['获取Haproxy记录', '增加/修改Haproxy记录', '删除Haproxy记录', '将修改写入到文件', '显示全部backend']
haproxy_file = "haproxy.conf"
indentation = 4
record_op_list = ['server','weight', 'maxconn']
record_op = {'server':"", 'weight':0 , 'maxconn':0}


conf_model = '''
global
        log 127.0.0.1 local2
        daemon
        maxconn 256
        log 127.0.0.1 local2 info
defaults
        log global
        mode http
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms
        option  dontlognull

listen stats :8888
        stats enable
        stats uri       /admin
        stats auth      admin:1234

frontend oldboy.org
        bind 0.0.0.0:80
        option httplog
        option httpclose
        option  forwardfor
        log global
        acl www hdr_reg(host) -i www.oldboy.org
        use_backend www.oldboy.org if www

{backends}
'''