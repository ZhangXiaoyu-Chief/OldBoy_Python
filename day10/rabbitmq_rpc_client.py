#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月23日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: RabbitMQ演示程序，RPC客户端

Help:
'''
import pika
import uuid

class FibonacciRpcClient(object):
    '''
    定义一个RpcClient类
    '''
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='10.10.1.133')) # 创建连接

        self.channel = self.connection.channel() # 创建channel
        # 定义接收返回的队列
        result = self.channel.queue_declare(exclusive = True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack = True,
                                   queue = self.callback_queue) # 调用消费方法，接收消息

    def on_response(self, ch, method, props, body):
        '''
        处理接收到的请求
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        '''
        if self.corr_id == props.correlation_id: # 判断收到的相应是否是我刚才发送请求的相应
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4()) # 生成一个随机字符串
        self.channel.basic_publish(exchange = '',
                                   routing_key = 'rpc_queue',
                                   properties = pika.BasicProperties(
                                         reply_to = self.callback_queue, # 定义回调队列
                                         correlation_id = self.corr_id, # 当此队列接收到一个响应的时候它无法辨别出这个响应是属于哪个请求的。correlation_id 就是为了解决这个问题而来的
                                         ),
                                   body = str(n)) # 相对队列发送请求
        while self.response is None:
            self.connection.process_data_events() # 接收相应的而数据，如果接收到将调用self.on_response处理相应的数据，如果获得正确的相应self.response的值会不为空，就会推出循环
        return int(self.response)

if __name__ == '__main__':
    fibonacci_rpc = FibonacciRpcClient() # 创建

    print(" [x] Requesting fib(30)")
    response = fibonacci_rpc.call(30)
    print(" [.] Got %r" % response)