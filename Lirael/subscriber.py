"""
    莉芮尔订阅坏狗发出的每一条tick信息
    本模块基于zeromq实现, 通过创建一个socket到指定端口, 我们可以收取坏狗群发的每一条tick信息
    用户还可以设置关键词来过滤我们不需要的tick信息
"""

import zmq


class Subscriber:
    """ 订阅者 """

    def __init__(self, tick_filter=""):
        """ 构造函数
            @param tick_filter 过滤器, 通过设置过滤器来滤掉不需要的tick信息
        """
        self.filter  = tick_filter
        self.context = None
        self.socket  = None

    def start(self, callback=None):
        """ 开始接收tick信息
            @param callback 设置一个回调函数, 每次接收有用的tick信息后, 都会调用此函数
        """
        if callback and not hasattr(callback, "__call__"):
            print("%s cannot be invoked" % str(callback))

        self.context = zmq.Context()
        self.socket  = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://192.168.61.8:16888")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        print("Subscriber is collecting tick information......")

        while True:
            tick_info = self.socket.recv_string()
            if callback:
                callback(tick_info)
            else:
                print(tick_info)

    def stop(self):
        """ 停止接收tick信息 """
        self.context.destroy()
        print("Subscriber has stopped, no more tick information will be collected.")


if __name__ == "__main__":
    sub = Subscriber(tick_filter="")
    sub.start()
