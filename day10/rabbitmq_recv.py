#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月22日

@author: 张晓宇

Email: 61411916@qq.com

Version: V1.0

Description: RabbitMQ hello word演示程序，接收方
Help:
'''
import pika
if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost')) # 创建连接对象
    channel = connection.channel() # 创建频道
    channel.queue_declare(queue='hello') # 创建队列
    def callback(ch, method, properties, body): # 定义一个函数
        print(" [x] Received %r" % body)
    # 调用方法basic_consume接收消息，callback是收到消息后做的操作，
    # 也就是收到消息后会自动调用这个函数，并把收到的消息作为参数传递
    # 个callback函数，queue表示接收消息的归类
    channel.basic_consume(callback,
                          queue = 'hello',
                          no_ack = True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming() #启动消费者 注意，这个方法阻塞循环接收消息