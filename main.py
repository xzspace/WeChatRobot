#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import signal

from wcferry import Wcf

from configuration import Config
from robot import Robot


def weather_report(robot: Robot) -> None:
    """模拟发送天气预报
    """

    # 获取接收人
    receivers = ["filehelper"]

    # 获取天气，需要自己实现，可以参考 https://gitee.com/lch0821/WeatherScrapy 获取天气。
    report = "这就是获取到的天气情况了"

    for r in receivers:
        robot.sendTextMsg(report, r)
        # robot.sendTextMsg(report, r, "nofity@all")   # 发送消息并@所有人


def main():
    config = Config()
    wcf = Wcf(debug=True)

    def handler(sig, frame):
        wcf.cleanup()  # 退出前清理环境
        exit(0)

    signal.signal(signal.SIGINT, handler)

    robot = Robot(config, wcf)
    robot.LOG.info("正在启动机器人···")

    # 机器人启动发送测试消息
    robot.sendTextMsg("机器人启动成功！", "filehelper")

    # 接收消息
    # robot.enableRecvMsg()     # 可能会丢消息？
    robot.enableReceivingMsg()  # 加队列

    # 每天 7 点发送天气预报
    robot.onEveryTime("07:00", weather_report, robot=robot)

    # 每天 7:30 发送新闻
    robot.onEveryTime("07:30", robot.newsReport)

    # 让机器人一直跑
    robot.keepRunningAndBlockProcess()


if __name__ == "__main__":
    main()
