import time
import lcm
import threading
from static.lcm import example_t


class PullLcmState:
    def __init__(self):
        self.state = 0
        self.name = ''
        self.lc = lcm.LCM()
        self.subscription = self.lc.subscribe("Analysis", self.analysis)

    def analysis(self, channel, data):
        msg = example_t.example_t.decode(data)
        self.state = str(msg.timestamp)
        self.name = str(msg.name)

    def run_lcm(self):
        try:
            while True:
                self.lc.handle()
        except KeyboardInterrupt:
            pass

    def run_analysis(self):
        new_thread = threading.Thread(target=self.run_lcm, name="T2")
        new_thread.start()


class PullLcmName:
    def __init__(self):
        self.name = ''
        self.lc = lcm.LCM()
        self.subscription = self.lc.subscribe("DataInfo", self.analysis)

    def analysis(self, channel, data):
        msg = example_t.example_t.decode(data)
        self.name = str(msg.name)
        time.sleep(1)

    def run_lcm(self):
        try:
            while True:
                self.lc.handle()
        except KeyboardInterrupt:
            pass

    def run_analysis(self):
        new_thread = threading.Thread(target=self.run_lcm, name="T4")
        new_thread.start()


class PushLcmState:
    def __init__(self):
        self.state = 0
        self.name = ''
        pass

    def analysis(self):
        msg = example_t.example_t()
        while True:
            msg.timestamp = self.state
            msg.name = self.name
            lc = lcm.LCM()
            lc.publish("Analysis", msg.encode())
            time.sleep(0.5)

    def run_analysis(self):
        new_thread = threading.Thread(target=self.analysis, name="T1")
        new_thread.start()


class PushLcmName:
    def __init__(self):
        self.name = ''
        pass

    def analysis(self):
        msg = example_t.example_t()
        while True:
            msg.name = self.name
            lc = lcm.LCM()
            lc.publish("DataInfo", msg.encode())
            time.sleep(0.5)

    def run_analysis(self):
        new_thread = threading.Thread(target=self.analysis, name="T3")
        new_thread.start()


# 发送状态
class PushLcmResult:
    def __init__(self):
        self.test_result = ''
        pass

    def analysis(self):
        msg = example_t.example_t()
        while True:
            msg.test_result = self.test_result
            lc = lcm.LCM()
            lc.publish("TestResult", msg.encode())
            time.sleep(0.5)

    def run_analysis(self):
        new_thread = threading.Thread(target=self.analysis, name="T4")
        new_thread.start()


# 接收状态
class PullLcmResult:
    def __init__(self):
        self.test_result = ''
        self.lc = lcm.LCM()
        self.subscription = self.lc.subscribe("TestResult", self.analysis)

    def analysis(self, channel, data):
        msg = example_t.example_t.decode(data)
        self.test_result = str(msg.test_result)
        time.sleep(1)

    def run_lcm(self):
        try:
            while True:
                self.lc.handle()
        except KeyboardInterrupt:
            pass

    def run_analysis(self):
        new_thread = threading.Thread(target=self.run_lcm, name="T4")
        new_thread.start()



if __name__ == '__main__':
    app = PushLcmState()
    app.run_analysis()
    ap = PushLcmName()
    ap.run_analysis()
    #发送状态
    time.sleep(5)
    app.state = 9
    time.sleep(8)
    app.state = 6
    time.sleep(5)
    #发送数据名称
    ap.name = 'wangbolun'
    time.sleep(6)
    ap.name = 'wangbolun11111111111111'

