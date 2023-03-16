import os
import time
from datetime import datetime


# 监控有没有新增程序或定时启动服务

def regular_run():
    while True:
        # 获取当前时间
        now = datetime.now()
        # 判断时间
        if now.strftime('%H:%M') == '08:57':
            # 执行任务
            os.system('python /home/dell/APP/CaseAnalysis/main.py')
            print('程序运行结束')
            time.sleep(61)

        else:
            time.sleep(10)
            print('当前时间为：' + str(now.strftime('%H:%M')) + str(' ,还未到达指定时间'))
            pass


if __name__ == '__main__':
    regular_run()
