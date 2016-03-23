#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月23日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: RabbitMQ演示程序 公平分发 发送端（生产者）

Help:
'''
import pika
import sys

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='10.10.1.133'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(exchange = '',
                          routing_key = 'task_queue',
                          body = message,
                          properties = pika.BasicProperties(
                             delivery_mode = 2, # 使消息持久化
                          ))
    print(" [x] Sent %r" % message)
    connection.close()