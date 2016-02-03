#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description:

Help:
'''
import logging
import os
if __name__ == '__main__':
    server_list = [
        {
            "name":"test",
            "script":"/et/init.d/api.smart",
            "port":8095
        }
    ]
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s [%(levelname)s] : %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='check_server.log', filemode='w')
    for server in server_list:
        server_name = server.get('name')
        server_script = server.get('script')
        server_port = server.get('port')
        server_status = os.popen('netstat -lnt|grep %s' %server_port)
        if not server_status:
            logging.info('%s is not avilable!' % server_name)
            os.popen('%s restart' %server_script)