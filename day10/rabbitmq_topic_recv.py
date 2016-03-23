#!/usr/bin/env python
# coding:utf-8
'''
Created on: 2016年3月23日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: RabbitMQ衍射程序  Publish\Subscribe(消息发布\订阅)演示程序，topic接收方

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

    result = channel.queue_declare(exclusive = True)
    queue_name = result.method.queue

    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys: # 遍历命令行参数，绑定多个topic
        channel.queue_bind(exchange = 'topic_logs',
                           queue = queue_name,
                           routing_key = binding_key) # 通过routing_key和exchange绑定queue

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

    channel.basic_consume(callback,
                          queue = queue_name,
                          no_ack = True)

    channel.start_consuming()