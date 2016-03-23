#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月22日

@author: 张晓宇

Email: 61411916@qq.com

Version: V1.0

Description: RabbitMQ hello word演示程序，发送方
Help:
'''
import pika # 导入pika包

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.10.1.133')) # 创建连接对象
    chan = connection.channel() # 创建频道对象
    chan.queue_declare(queue = 'hello') # 创建一个队列queue命名为hello
    chan.basic_publish(exchange = '',
                          routing_key = 'hello',
                          body = 'hello word') # 发送一条消息，routing_key表示表示往hello这个队列发送， body是消息的内容，exchange是
    print(" [x] Sent 'hello word'")
    connection.close() # 关闭连接