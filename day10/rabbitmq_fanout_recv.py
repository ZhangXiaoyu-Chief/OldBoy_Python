#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月23日

@author: 张晓宇

Email: 61411916@qq.com

Version: V1.0

Description: RabbitMQ Publish\Subscribe(消息发布\订阅)演示程序，fanout接收方
Help:
'''
import pika

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   '10.10.1.133'))
    channel = connection.channel()
    # 声明exchange
    channel.exchange_declare(exchange = 'logs',
                         type = 'fanout')
    # 声明queue，不指定queue名字，rabbit会随机分配一个名字，
    # exclusive=True会在使用此queue的消费者断开后，自动将queue删除
    result = channel.queue_declare(exclusive = True)
    queue_name = result.method.queue # 获取queue的名称用于下一条语句

    channel.queue_bind(exchange = 'logs',
                       queue = queue_name) # 把刚才随机获取的queue和exchange绑定

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] %r" % body)

    channel.basic_consume(callback,
                          queue = queue_name,
                          no_ack = True)

    channel.start_consuming()