#!/usr/bin/env python3
# coding:utf-8
'''
Created on: 2016年3月14日

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description: select demo

Help:
'''
import select # 导入select模块，既然是select demo当然要导入select模块了
import socket # 导入socket模块，这里用socket做示例演示异步IO
import sys # 导入sys模块
import queue # 导入queue模块

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建服务端socket对象，socket.AF_INET表示IPv4，socket.SOCK_STREAM表示流式socket也就是TCP
server.setblocking(False) # 将服务端设置成非阻塞式的

# Bind the socket to the port
server_address = ('localhost', 8888) # 设置监听的地址和端口
print(sys.stderr, 'starting up on %s port %s' % server_address) # 打印服务端启动信息

server.bind(server_address) # 绑定监听的地址和端口

# Listen for incoming connections
server.listen(5) # 启动监听，5代表可以同时有5个客户端，可以建立连接

# Sockets from which we expect to read
inputs = [ server ] # 将server端的socket对象加入到inputs列表

# Sockets to which we expect to write
outputs = [ ] # 建立一个空列表

message_queues = {} # 创建一个空的消息队列
while inputs: # 只要inputs列表不为空，就循环，inputs里面如果为空说明连服务端的socket对象也异常，程序出现了问题，退出循环也就退出了整个服务端

    # Wait for at least one of the sockets to be ready for processing
    print( '\nwaiting for the next event') # 打印
    '''
    调用select.select方法接受3个参数
    select()方法接收并监控3个通信列表，
        1、所有的输入的data,就是指外部发过来的数据，
        2、监控和接收所有要发出去的data(outgoing data),
        3、监控错误信息，接下来我们需要创建2个列表来包含输入和输出信息来传给select().
    同时返回新的select方法处理过的
    '''
    readable, writable, exceptional = select.select(inputs, outputs, inputs) # 程序会阻塞在这里（我的理解是会会阻塞到监控状态发生变化，也就是readable,writeable,exceptional三个列表至少有一个列表有成员），这里的阻塞不是来自于socket对象，而是来自于select，模块，一旦列表发生变化，才会继续
    # Handle inputs
    print(readable)
    print(writable)
    print(exceptional)
    print(inputs)
    print(outputs)
    for s in readable: # 循环readable列表里的socket对象
        if s is server: # 如果socket对象是服务端的socket对象，说明是有一个新的连接
            # A "readable" server socket is ready to accept a connection
            connection, client_address = s.accept() # 获取客户端的socket对象和客户单地址和端口
            print('new connection from', client_address) # 输出来自客户端的链接信息
            connection.setblocking(False) # 将客户端的socket对象也设置成非阻塞式的
            inputs.append(connection) # 将客户端对象加入到inputs列表，用来while下一次循环的时候加入到select的监控

            # Give the connection a queue for data we want to send
            print(connection)
            message_queues[connection] = queue.Queue() # 将客户端socket对象connection作为key一个新的Queue对象作为value加入到消息字典中，这个Queue用来保存要传递给客户端的消息
        else:
            '''
            若果不是服务端socket对象，说明是客户端的socket，也就是客户端口发过来数据了，我们可以读了
            '''
            data = s.recv(1024) # 获取端口发送过来的数据
            if data: # 如果获取到的内容不为空，说明客户端正常
                # A readable client socket has data
                print(sys.stderr, 'received "%s" from %s' % (data, s.getpeername()) ) # 打印错误输出和从客户端接受到的数据
                message_queues[s].put(data) # 将获取到内容原样放到消息队列中，稍后再发送给客户端
                # Add output channel for response
                if s not in outputs: # 如果这个客户端，不在output列表（也就是输出列表中）
                    outputs.append(s) # 就把他加进去
            else:
                # 若果接受到内容为空，说明客户端遇到异常关闭
                # Interpret empty result as closed connection
                print('closing', client_address, 'after reading no data') # 输出关闭消息
                # Stop listening for input on the connection
                if s in outputs: # 如果这个断开的客户端socket对象在output列表（也就是输出列表中）
                    outputs.remove(s)  # 将他移除出去，既然客户端都断开了，我就不用再给它返回数据了，所以这时候如果这个客户端的连接对象还在outputs列表中，就把它删掉
                inputs.remove(s)    # inputs中也删除掉（也就不用监听他的输入）
                s.close()           # 把这个连接关闭掉

                # Remove message queue
                del message_queues[s] # 删除这个客户端所对应的消息队列，释放空间
    # Handle outputs
    for s in writable: # 遍历writable列表
        #print(writable)
        try: # 捕获queue为空异常，只要不为空就说明有数据要发
            next_msg = message_queues[s].get_nowait() # 从对应的队列中获取要发送的消息
        except queue.Empty:
            # 如果队列为空，说明消息都已经发送完毕了
            # No messages waiting so stop checking for writability.
            print('output queue for', s.getpeername(), 'is empty') # 打印为空消息
            outputs.remove(s) # 将该socket对象移出输出监控队列
        else:
            # 如果不为空，说明还有消息要发
            print('sending "%s" to %s' % (next_msg, s.getpeername())) # 打印发送消息 getpeername方法获取客户端socket的ip地址和端口，和服务端端socket
            s.send(next_msg) # 发送消息
    # Handle "exceptional conditions"
    for s in exceptional: # 遍历异常列表
        print('handling exceptional condition for', s.getpeername() ) # 获取异常消息
        # Stop listening for input on the connection
        inputs.remove(s) # 移出input列表，不在监控
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]
    print('循环结束')