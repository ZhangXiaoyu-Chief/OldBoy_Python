#!/usr/bin/env python
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description:

Help:
'''
class WebSerber(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def host(self):
        print('host')

    def start(self):
        print('Server is starting...')

    def stop(self):
        print('Server is stoping...')

    def restart(self):
        self.stop()

def test_run():
    print('running...')

if __name__ == '__main__':
    server = WebSerber('localhost', 8080)
    if hasattr(server, 'host'):
        print(getattr(server, 'restart'))
        print(server.restart)
        getattr(server, 'start')()
    setattr(server, 'test_run', test_run)
    server.test_run()
    print(server.port)
    #delattr(server, 'porft')
    print(server.port)
    print(getattr(server, 'host'))
