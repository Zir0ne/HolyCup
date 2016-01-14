"""
    入口文件
"""

import subscriber


if __name__ == "__main__":
    # 启动后, 应当首先从历史数据文件中恢复足够多的相应货币对的历史数据
    # 由于目前运行MT4的系统与Lirael系统不是同一个, 暂且将这个任务延后完成

    # 启动市场数据接收器
    listener = subscriber.Subscriber()
    listener.start()

