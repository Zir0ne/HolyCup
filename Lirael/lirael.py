"""
    入口文件
"""

import subscriber
import request
import pool
import zmq
import time
import json


# 信号格式
# chart_id: oChart_货币对_周期_表格ID_是否为EA
# tick:      tick|chart_id|0|时间|json|.....
# bar:        bar|chart_id|0|时间|json|.....
# timer:    timer|chart_id|0|时间|json|.....
def dispatcher(tick):
    """ 将交易信号进行处理, 分发给相应的函数
        @param tick  交易信号, 字符串形式
    """
    try:
        tick_parts  = tick.split(sep="|")
        chart_parts = tick_parts[1].split(sep="_")
        # EA标识, 如果不为1, 说明这条信息不是由EA发出的, 此时不应当处理
        if chart_parts[4] != "1":
            return
        # 获取携带的信息
        symbol   = chart_parts[1]
        period   = chart_parts[2]
        chart_id = chart_parts[3]
        elapsed  = tick_parts[3]
        info     = json.loads(tick_parts[5]) if "json" == tick_parts[4] else None
        # 执行分发
        if "tick" in tick_parts[0]:
            print("found tick")
        elif "bar" in tick_parts[0]:
            print("found bar")
        elif "timer" in tick_parts[0]:
            print("found timer")
    except json.JSONDecodeError:
        print("Invalid json format data found!")


if __name__ == "__main__":
    # 创建进程唯一的通信上下文
    context = zmq.Context()
    # 生成指令发送器
    requester = request.Request(context, "tcp://192.168.61.8:16999")
    # 启动数据中心
    data_center = pool.Pool(requester)
    # 启动市场数据接收器
    listener = subscriber.Subscriber(context, "tcp://192.168.61.8:16888")
    listener.start(dispatcher)
    time.sleep(300)
    listener.stop()


