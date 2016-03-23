#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月23日

@author: 张晓宇

Email: 61411916@qq.com

Version: V1.0

Description: RabbitMQ Publish\Subscribe(消息发布\订阅)演示程序，fanout发送方
Help:
'''
import pika
import sys
if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   '10.10.1.133'))
    channel = connection.channel()

    #声明queue
    channel.queue_declare(queue = 'task_queue', durable = True)
    channel.exchange_declare(exchange = 'logs', # exchange的名称
                         type = 'fanout') # 声明exchange类型为fanout
    message = ' '.join(sys.argv[1:]) or "Hello World!" # 通过命令行接收要发送的消息
    channel.basic_publish(exchange = 'logs', # 这里就不能为空了，得往我们刚才声明的exchange里发送
                      routing_key = 'task_queue',
                      body = message,
                      properties = pika.BasicProperties(
                         delivery_mode = 2,
                      ))
    print(" [x] Sent %r" % message)
    connection.close()