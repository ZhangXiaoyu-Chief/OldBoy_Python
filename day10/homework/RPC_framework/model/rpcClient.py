#!/usr/bin/env python
# coding:utf-8
import pika
import uuid
from conf import conf
class rpcClient(object):
    '''
    定义一个RpcClient类
    '''
    def __init__(self):
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
                host= conf.RBMQ_HOST)) # 创建连接

        self.__channel = self.__connection.channel() # 创建channel
        self.__channel.exchange_declare(exchange = 'rpc_ex',
                         type = 'fanout')
        # 定义接收返回的队列
        self.__channel.queue_declare(queue = 'rpc_que', exclusive = True)
        result = self.__channel.queue_declare(exclusive = True)
        self.__callback_queue = result.method.queue
        print(self.__callback_queue)

        self.__channel.basic_consume(self.__on_response, no_ack = True,
                                   queue = self.__callback_queue) # 调用消费方法，接收消息

    def __on_response(self, ch, method, props, body):
        '''
        处理接收到的请求
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        '''
        # print(method)
        # print(props)
        # print(ch)
        # from libs import mylib
        # print(type(body))
        print()
        if self.__corr_id == props.correlation_id: # 判断收到的相应是否是我刚才发送请求的相应
            print(str(eval(body), encoding='utf8'))

    def call(self, n):
        self.__response = None
        self.__corr_id = str(uuid.uuid4()) # 生成一个随机字符串
        self.__channel.basic_publish(exchange = 'rpc_ex',
                                   routing_key = 'rpc_que',
                                   properties = pika.BasicProperties(
                                         delivery_mode = 2,
                                         reply_to = self.__callback_queue, # 定义回调队列
                                         correlation_id = self.__corr_id, # 当此队列接收到一个响应的时候它无法辨别出这个响应是属于哪个请求的。correlation_id 就是为了解决这个问题而来的
                                         ),
                                   body = str(n)) # 相对队列发送请求
        #while self.__response is None:
        self.__connection.process_data_events() # 接收相应的而数据，如果接收到将调用self.on_response处理相应的数据，如果获得正确的相应self.response的值会不为空，就会推出循环
        # while True:
        #     self.__connection.process_data_events()
        count = 0
        import time
        # print(self.__channel)
        # print(self.__channel.channel_number)
        # print(self.__channel._queue_consumer_generator)
        #print(self.__channel.start_consuming())
        time.sleep(5)
        self.__connection.process_data_events()
        # while True:
        #     time.sleep(5)
        #     self.__connection.process_data_events()
        #     break


        # print(self.__response)
        # print(self.__response.decode())
        # return self.__response.decode()
