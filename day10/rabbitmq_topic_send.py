#!/usr/bin/env python
# coding:utf-8
'''
Created on: 2016年3月23日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: RabbitMQ衍射程序  Publish\Subscribe(消息发布\订阅)演示程序，topic发送方

Help:
'''
import pika
import sys
if __name__ == '__main__':

    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='10.10.1.133'))
    channel = connection.channel()

    channel.exchange_declare(exchange = 'topic_logs',
                         type = 'topic') # 声明exchange，类型topic

    routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info' # 从命令行获取topic
    message = ' '.join(sys.argv[2:]) or 'Hello World!'
    channel.basic_publish(exchange = 'topic_logs',
                          routing_key = routing_key, # 发送到指定routing_key
                          body = message)
    print(" [x] Sent %r:%r" % (routing_key, message))
    connection.close()