"""
    莉芮尔订阅坏狗发出的每一条tick信息
    本模块基于zeromq实现, 通过创建一个socket到指定端口, 我们可以收取坏狗群发的每一条tick信息
    用户还可以设置关键词来过滤我们不需要的tick信息
"""

import zmq
import threading


class Subscriber:
    """ 订阅者 """

    def __init__(self, context, address, tick_filter=""):
        """ 构造函数
            @param context     通信上下文, 进程唯一
            @param address     发送tick信息的服务器的地址
            @param tick_filter 过滤器, 通过设置过滤器来滤掉不需要的tick信息
        """
        self.filter   = tick_filter
        self.context  = context
        self.address  = address
        self.socket   = None
        self.handler  = None
        self.quit_event = threading.Event()
        self.quit_event.clear()

    def start(self, callback=None):
        """ 开始接收tick信息
            @param callback 设置一个回调函数, 每次接收有用的tick信息后, 都会调用此函数, 如果不提供, 仅仅打印tick信息
        """
        if callback and not hasattr(callback, "__call__"):
            print("%s cannot be invoked" % str(callback))
            return
        # 如果工作线程已经存在, 应当首先关闭, 再创建新的
        if self.handler and not self.quit_event:
            self.quit_event.set()
            self.handler.join()
        # 开启工作线程
        self.quit_event.clear()
        self.handler = threading.Thread(target=Subscriber.work_thread,
                                        args=(None, self.context, self.address, self.quit_event, callback))
        self.handler.start()

    def stop(self):
        """ 停止接收tick信息 """
        if self.handler:
            self.quit_event.set()
            self.handler.join()
            self.handler = None

    def work_thread(self, *args):
        """ 工作线程 """
        # 准备socket
        socket = args[0].socket(zmq.SUB)
        socket.connect(args[1])
        socket.setsockopt_string(zmq.SUBSCRIBE, '')
        print("Subscriber is collecting tick information......")
        # 工作循环
        quit_event = args[2]
        callback   = args[3]
        while not quit_event.is_set():
            tick_info = socket.recv_string()
            if callback:
                callback(tick_info)
            else:
                print(tick_info)
        # 退出, 清除资源
        socket.close()
        quit_event.clear()
        print("Subscriber has stopped, no more tick information will be collected.")


if __name__ == "__main__":
    sub = Subscriber(zmq.Context(), "tcp://192.168.61.8:16888", tick_filter="")
    sub.start()
