from twisted.internet import reactor, protocol


# a client protocol

class EchoClient(protocol.Protocol): # 同样继承protocol.Protocol类，重写里面的方法
    """Once connected, send a message, then print the result."""

    def connectionMade(self):
        # 重写connectionMade方法，当连接建立起来的时候想服务端发送一条消息
        self.transport.write(b"hello alex!")

    def dataReceived(self, data):
        # 重写dataReceived方法，当接受到消息的时候打印到屏幕，并关闭消息
        "As soon as any data is received, write it back."
        print("Server said:", data.decode()) # 打印消息
        self.transport.loseConnection() # 关闭连接

    def connectionLost(self, reason):
        # 重写connectionLost方法，当连接关闭的时候执行
        print("connection lost") # 打印练级关闭消息

class EchoFactory(protocol.ClientFactory): # 继承自protocol.ClientFactory，与服务端不同的是从新定义了客户端工厂类，重写了一些方法
    protocol = EchoClient # protocol等于我们刚才定义的类，这里也可以写到示例话之后

    def clientConnectionFailed(self, connector, reason):
        # 客户端建立连接失败调用此方法
        print("Connection failed - goodbye!22")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        # 客户端失去连接是调用此方法
        print("Connection lost - goodbye!")
        reactor.stop()


# this connects the protocol to a server running on port 8000
def main():
    # 剩下的就和服务端一样了，除了protocol在定义类的时候精制定了，当然，也可以在这里f.protocol = EchoClient指定
    f = EchoFactory()
    reactor.connectTCP("localhost", 1234, f)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()