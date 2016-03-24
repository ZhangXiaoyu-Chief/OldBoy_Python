#!/usr/bin/env python
# coding:utf-8
import pika
import uuid
from conf import conf
from libs import mylib
class rpcClient(object):
    '''
    定义一个RpcClient类
    '''
    def __init__(self):
        self.__log = mylib.mylog(conf.CLIENT_LOG)
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
                host= conf.RBMQ_HOST)) # 创建连接
        self.__channel = self.__connection.channel() # 创建channel
        self.__channel.exchange_declare(exchange = conf.EXCHANGE,
                         type = 'fanout') # 定义exchange
        self.__channel.queue_declare(queue = conf.QUEUE, exclusive = True)
        result = self.__channel.queue_declare(exclusive = True)
        self.__callback_queue = result.method.queue # 定义接收返回的队列
        #print(self.__callback_queue)

        self.__channel.basic_consume(self.__on_response, no_ack = True,
                                   queue = self.__callback_queue) # 调用消费方法，接收消息

    def __on_response(self, ch, method, props, body):
        '''
        回调函数，收到数据后将会自动调用该方法，处理接收到的请求
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        '''
        if self.__corr_id == props.correlation_id: # 判断收到的相应是否是我刚才发送请求的相应
            print(str(body, 'utf8'))

    def call(self, cmd):
        '''
        模块主入口
        :param cmd: 要远端服务器执行的命令
        :return:
        '''
        self.__response = None
        self.__corr_id = str(uuid.uuid4()) # 生成一个随机字符串
        self.__log.info('excute commend %s' %cmd)
        self.__channel.basic_publish(exchange = conf.EXCHANGE,
                                   routing_key = conf.QUEUE,
                                   properties = pika.BasicProperties(
                                         delivery_mode = 2,
                                         reply_to = self.__callback_queue, # 定义回调队列
                                         correlation_id = self.__corr_id, # 当此队列接收到一个响应的时候它无法辨别出这个响应是属于哪个请求的。correlation_id 就是为了解决这个问题而来的
                                         ),
                                   body = cmd) # 相对队列发送请求
        import time
        time.sleep(conf.TIME_OUT) # 设置超时，如果超过这个时间都就被丢弃了
        self.__connection.process_data_events() # 接收相应的而数据
