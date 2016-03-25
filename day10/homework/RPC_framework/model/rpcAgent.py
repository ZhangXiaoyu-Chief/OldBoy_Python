#!/usr/bin/env python
# coding:utf-8
import pika
from conf import conf
from libs import mylib
class rpcAgent(object):
    def __init__(self):
        '''
        构造方法
        :return: 无
        '''
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
        host = conf.RBMQ_HOST )) # 创建连接
        self.__log = mylib.mylog(conf.AGENT_LOG)
        self.__channel = self.__connection.channel() # 创建channel
        self.__channel.exchange_declare(exchange = conf.EXCHANGE,
                         type = 'fanout')
        res = self.__channel.queue_declare(durable = True) # 队列持久化
        self.__queue_name = res.method.queue

    def __run_commend(self, commend):
        '''
        运行命令方法
        :param commend: 要执行的命令
        :return: 返回命令执行的结果
        '''
        import subprocess
        try:
            p = subprocess.Popen(commend, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            error = p.stderr.read()
            if not error:
                res = p.stdout.read() # 读取命令执行的结果
            else:
                res = error
            res = str(res, 'utf8')
        except Exception as e:
            res = e
        print(res)
        return '[%s]\n%s' %(conf.AGENT_NAME, res)

    def __on_request(self, ch, method, props, body):
        '''
        回调方法，当收到消息的时候将自动调用这个方法
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        '''
        commend = body.decode()
        self.__log.info('run commend %s' %body.decode())
        response = self.__run_commend(commend)
        ch.basic_publish(exchange = '',
                         routing_key = props.reply_to,
                         properties = pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         body = str(response)) # 发送消息
        ch.basic_ack(delivery_tag = method.delivery_tag) # 通知消息消费完了

    def run(self):
        '''
        agent入口方法
        :return:
        '''
        self.__channel.queue_bind(exchange = conf.EXCHANGE,
                       queue = self.__queue_name) # 绑定queue和exchange
        self.__channel.basic_consume(self.__on_request, queue = self.__queue_name) # 接收消息

        print(" [x] Awaiting RPC requests")
        self.__channel.start_consuming() # 等待接收消息
