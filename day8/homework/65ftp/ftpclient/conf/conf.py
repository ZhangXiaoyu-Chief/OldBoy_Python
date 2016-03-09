#!/usr/bin/env python
# coding:utf-8

import socketserver

import os

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

SERVER_IP = '127.0.0.1'

FILE_PER_SIZE = 1024

PORT = 9998

USER_FILE = 'dbs/user.db'

LOGS = 'logs/65ftp_server.log'

DEFAULT_QUOTA = 500




