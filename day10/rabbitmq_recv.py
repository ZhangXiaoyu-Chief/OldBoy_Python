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


    #You may ask why we declare the queue again ‒ we have already declared it in our previous code.
    # We could avoid that if we were sure that the queue already exists. For example if send.py program
    #was run before. But we're not yet sure which program to run first. In such cases it's a good
    # practice to repeat declaring the queue in both programs.
    #channel.queue_declare(queue='hello', durable = True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=True) # callback 是收到消息后做的操作

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()