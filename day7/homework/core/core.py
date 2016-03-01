#!/usr/bin/env python
# coding:utf-8
from model.server import myftp
def run():
    server = myftp()
    server.runserver()
    print('run')