#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月23日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: RabbitMQ演示程序，RPC服务端

Help:
'''
import pika
import time

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='10.10.1.133')) # 创建连接

    channel = connection.channel() # 创建channel

    channel.queue_declare(queue='rpc_queue') # 声明队列

    def fib(n):
        '''
        求斐波拉契数列的函数，也是这个示例要远程执行的
        :param n: 斐波拉契长度
        :return: 斐波拉契数列
        '''
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fib(n-1) + fib(n-2)

    def on_request(ch, method, props, body):
        '''
        定义函数，用于channel.basic_consume的回调
        :param ch:
        :param method:
        :param props:
        :param body: 消息体
        :return: 无
        '''
        n = int(body)

        print(" [.] fib(%s)" % n)
        response = fib(n) # 调用fib函数获取斐波拉契数列
        print(props.correlation_id)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         body = str(response)) # 发送消息
        ch.basic_ack(delivery_tag = method.delivery_tag) # 通知消息消费完了

    channel.basic_qos(prefetch_count = 1)
    channel.basic_consume(on_request, queue = 'rpc_queue')

    print(" [x] Awaiting RPC requests")
    channel.start_consuming() # 等待接收消息