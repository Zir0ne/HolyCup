"""
    提供接口, 使得莉芮尔可以给坏狗发出指令, 同时接收指令的执行结果
    本模块基于zeromq实现
    模块提供多种指令的格式化功能, 只要调用相应的函数即可
"""

import zmq


class Request:
    """ 每一个实例代表发送指令的一个通道, 所有通道共享进程的通信上下文 """
    def __init__(self, context, address):
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(address)

    def send(self, request):
        """ 发送指令, 同时接收指令执行结果
            @param  request 指令, 字符串形式
            @return         指令的执行结果, 字符串形式
        """
        self.socket.send_string(request)
        return self.socket.recv_string()

    def retrive_bar(self, symbol, period, number):
        """ 发送指令, 获取bar信息
            @param symbol 货币对
            @param period 周期
            @param number 数量, 表示从当前bar开始(包含), 向前获取多少数量的bar
            @return       bar序列如果成功, 否则None
        """
