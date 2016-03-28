#!/usr/bin/env python3
# coding:utf-8
import paramiko
import sys
import traceback
from paramiko.py3compat import input
import interactive
class myTty(object):
    def __init__(self, ip, username, port, pawword, rsa_key = None):
        self.username = username
        self.ip = ip
        self.port = port
        self.rsa_key = rsa_key
        self.password = password

    def get_ssh(self, ip, port, username, rsa_key_file = None):
        # now, connect and use paramiko Client to negotiate SSH2 across the connection
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if rsa_key_file and os.path.isfile(rsa_key_file)
                client.connect(ip, port = port, username = password, key_filename = rsa_key_file, look_for_keys = False)
                return client
            else:
                client.connect(ip, port = port, username = password, look_for_keys = False)
                return client
        except Exception as e:
            return None
    def run(self):
        chan = client.invoke_shell()
        interactive.interactive_shell(chan)
        chan.close()
        client.close()
