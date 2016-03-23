#!/usr/bin/env python
# coding:utf-8
'''
Created on: 2016年3月23日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: RabbitMQ衍射程序  Publish\Subscribe(消息发布\订阅)演示程序，direct接收方

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

    result = channel.queue_declare(exclusive = True) # 随机声明queue
    queue_name = result.method.queue # 获取queue名称

    severities = sys.argv[1:] # 获取命令行参数，确定接收什么关键字消息
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    for severity in severities: # 遍历参数，可以绑定多个关键字
        channel.queue_bind(exchange = 'direct_logs',
                           queue = queue_name,
                           routing_key = severity)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body)) # method.routing_key表示获取的关键字

    channel.basic_consume(callback,
                          queue = queue_name,
                          no_ack = True)

    channel.start_consuming()