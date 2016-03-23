#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月23日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: RabbitMQ演示程序 公平分发 接收端（消费者）

Help:
'''
import pika
import time

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='10.10.1.133'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count = 1) # 主要变化在这里，这里等于告诉RabbitMQ没消费完别再给我消息
    channel.basic_consume(callback,
                          queue='task_queue')

    channel.start_consuming()