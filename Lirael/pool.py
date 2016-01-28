"""
    数据中心, 依照货币对, 周期等分类存放bar的信息, 以及所有与交易有关的数据
"""

import zmq
import request


class Pool:
    """ 分类管理数据, 对外提供获取数据的接口 """
    def __init__(self, r):
        """ 构造函数 """
        self.bars = dict()
        self.r    = r

    def new(self, symbol, period, bar):
        """ 调用此函数来将新的bar信息记录到数据中心
            @param symbol 货币对, 字符串形式
            @param period 周期, 字符串形式
            @param bar    bar信息
        """
        bar_type = symbol + "_" + period
        # 如果之前已经记录过这种类型的bar, 将新的数据加入即可, 加入的时候应当检查序列的连续性
        if bar_type in self.bars:
            pass
        # 否则, 创建一个新的序列, bar作为第一个元素加入
        else:
            self.bars[bar_type] = [bar, ]

    def __request(self, symbol, period, number):
        """ 联系EA, 主动获取指定货币对和周期的bar信息
            @param symbol 货币对
            @param period 周期
            @param number 数量, 表示从当前bar开始(包含), 向前获取多少数量的bar
            @return       bar序列如果成功, 否则None
        """
        return self.r.retrive_bar(symbol, period, number)
