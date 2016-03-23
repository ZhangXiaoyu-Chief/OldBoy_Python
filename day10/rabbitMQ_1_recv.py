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
import pika,time
if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   '10.10.1.133'))
    channel = connection.channel()
    data = None
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body) # 打印消息
        time.sleep(body.count(b'.')) # 假设执行了多少秒（有多少.就sleep多少秒）\
        global data
        data = body
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag) # 回复执行完了


    channel.basic_consume(callback,
                          queue='task_queue',
                          )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    while data is None:
        print(data)
        connection.process_data_events()