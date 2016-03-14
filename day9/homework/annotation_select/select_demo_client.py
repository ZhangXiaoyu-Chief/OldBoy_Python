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
__author__ = 'jieli'
import socket
import sys

messages = [ 'This is the message. ',
             'It will be sent ',
             'in parts.',
             ]
server_address = ('localhost', 8888)

# Create a TCP/IP socket
socks = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM),
          #socket.socket(socket.AF_INET, socket.SOCK_STREAM),
          ]

# Connect the socket to the port where the server is listening
print(sys.stderr, 'connecting to %s port %s' % server_address)

for s in socks:
    #s.getpeername()
    s.connect(server_address)

# for message in messages:
#
#     # Send messages on both sockets
#     for s in socks:
#         print(sys.stderr, '%s: sending "%s"' % (s.getsockname(), message))
#         s.send(bytes(message, 'utf8'))
#
#     # Read responses on both sockets
#     for s in socks:
#         data = s.recv(1024)
#         print(sys.stderr, '%s: received "%s"' % (s.getsockname(), data))
#         if not data:
#             print(sys.stderr, 'closing socket', s.getsockname())
#             s.close()
while True:
    message = input('>>: ')
    if message == 'exit':
        break
    for s in socks:
        print(sys.stderr, '%s: sending "%s"' % (s.getsockname(), message))
        s.send(bytes(message, 'utf8'))
    # for s in socks:
    #     #data = s.recv(1024)
    #     data =
    #     print(sys.stderr, '%s: received "%s"' % (s.getsockname(), data))
    #     if not data:
    #         print(sys.stderr, 'closing socket', s.getsockname())
s.close()
