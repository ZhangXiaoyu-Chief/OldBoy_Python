#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月22日

@author: 张晓宇

Email: 61411916@qq.com

Version: V1.0

Description: RabbitMQ work queue演示程序，接收方
Help:
'''
import pika, time
if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   '10.10.1.133')) # 创建连接对象
    channel = connection.channel() # 创建频道
    channel.queue_declare(queue='task_q') # 创建队列
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_consume(callback,
                          queue = 'task_queue',
                          no_ack = True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()