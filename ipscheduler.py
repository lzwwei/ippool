'''
调度模块，不停循环前三个模块
'''
import time
from multiprocessing import Process
from IPapi import app
from Getter import Getter
from testip import TestIp


class Scheduler(object):
    def __init__(self):
        self.test_switch = True
        self.getter_switch = True
        self.api_switch = True

    def schedule_test(self, cycle=20):
        tester = TestIp()
        while True:
            print('测试IP开始')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=20):
        getter = Getter()
        while True:
            print('获取IP开始')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run('127.0.0.1',8888)

    def run(self):
        print('开始运行进程池！！！')
        if self.getter_switch:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if self.test_switch:
            tester_process = Process(target=self.schedule_test)
            tester_process.start()

        if self.api_switch:
            api_process = Process(target=self.schedule_api)
            api_process.start()

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()