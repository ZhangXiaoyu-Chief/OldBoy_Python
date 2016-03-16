#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 

Description: 
Help:
'''

if __name__ == '__main__':
    import pika

    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
    channel = connection.channel()

    #声明queue
    channel.queue_declare(queue='task_queue')

    #n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
    import sys

    message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message,
                          properties=pika.BasicProperties(
                          delivery_mode = 2, # make message persistent
                          ))
    print(" [x] Sent %r" % message)
    connection.close()