#!/usr/bin/env python
# coding:utf-8
import pika
from conf import conf
from libs import mylib
class rpcAgent(object):
    def __init__(self):
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
        host = conf.RBMQ_HOST )) # 创建连接
        self.__log = mylib.mylog(conf.AGENT_LOG)
        self.__channel = self.__connection.channel() # 创建channel
        self.__channel.exchange_declare(exchange = 'rpc_ex',
                         type = 'fanout')
        #channel.queue_declare(queue = 'task_queue', durable = True)
        res = self.__channel.queue_declare(durable = True) # 队列持久化
        self.__queue_name = res.method.queue

    def __run_commend(self, commend):
        '''
        运行命令方法
        :param commend: 要执行的命令
        :return: 返回命令执行的结果
        '''
        import subprocess
        p = subprocess.Popen(commend, shell=True, stdout=subprocess.PIPE)
        res = p.stdout.read()
        res = str(res, 'utf8')
        #res = str(res, 'utf8')
        # res = ("jjj\n%s" %str(eval(res), 'utf8'))
        #print(str(res, 'utf8'))
        print(res)
        return '[%s]\n%s' %(conf.AGENT_NAME, res)
        #return 'eee'

    def __on_request(self, ch, method, props, body):
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
        #self.__channel.basic_qos(prefetch_count = 1)
        #self.__queue_name = result.method.queue # 获取queue的名称用于下一条语句

        self.__channel.queue_bind(exchange = 'rpc_ex',
                       queue = self.__queue_name)
        #self.__channel.queue_bind(exchange = 'rpc_ex',
        #               queue = conf.QUEUE)
        self.__channel.basic_consume(self.__on_request, queue = self.__queue_name)

        print(" [x] Awaiting RPC requests")
        self.__channel.start_consuming() # 等待接收消息
