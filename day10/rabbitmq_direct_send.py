#!/usr/bin/env python
# coding:utf-8
'''
Created on: 2016年3月23日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: RabbitMQ衍射程序  Publish\Subscribe(消息发布\订阅)演示程序，direct发送方

Help:
'''
import pika
import sys
if __name__ == '__main__':

    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='10.10.1.133'))
    channel = connection.channel()

    channel.exchange_declare(exchange = 'direct_logs',
                             type = 'direct') # 声明exchange，类型direct

    severity = sys.argv[1] if len(sys.argv) > 1 else 'info' # 通过命令行获取关键字
    message = ' '.join(sys.argv[2:]) or 'Hello World!'
    channel.basic_publish(exchange = 'direct_logs',
                          routing_key = severity, # 这里指定routing_key为获取的关键字
                          body = message)
    print(" [x] Sent %r:%r" % (severity, message))
    connection.close()