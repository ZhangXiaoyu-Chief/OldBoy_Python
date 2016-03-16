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
import pika


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
    channel = connection.channel()

    #声明queue
    #channel.queue_declare(queue='hello', durable = True)

    #n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
    while True:
        data = input('>> ')
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=data)
        print(" [x] Sent '%s'" %data)
    connection.close()