#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月22日

@author: 张晓宇

Email: 61411916@qq.com

Version: V1.0

Description: RabbitMQ work queue演示程序，发送方
Help:
'''
import pika
import sys
if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   '10.10.1.133'))
    channel = connection.channel()
    #声明queue
    channel.queue_declare(queue='task_queue')
    #RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
    message = ' '.join(sys.argv[1:]) or "Hello World! 33"
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body = message,
                          properties = pika.BasicProperties(
                          delivery_mode = 2, # 使消息持久
                          ))
    print(" [x] Sent %r" % message)
    connection.close()