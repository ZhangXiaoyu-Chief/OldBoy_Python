#!/usr/bin/env python
# coding:utf-8

import os

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOME_PATH = '%s/home' %BASE_DIR

CODE_LIST = {
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
    '401': "Invalid instruction!",
    '500': "Invalid execute successful",
    '501': "Invalid execute fail",
}

SERVER_IP = '0.0.0.0'

PORT = 9998

USER_FILE = 'dbs/users.db'

LOGS = 'logs/65ftp_server.log'

DEFAULT_QUOTA = 500

FILE_PER_SIZE = 1024

